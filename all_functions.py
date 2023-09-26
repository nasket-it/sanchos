from numba import njit

from AlorPy import AlorPy  # Работа с Alor OpenAPI V2
from Config import *
from keywords import Keywords, Risck
import openai
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import time
import re
from datetime import datetime
import requests
from audio_text import audio_to_text, convert_ogg_wav
import os
import asyncio

# print(datetime.now().second , datetime.now().microsecond)
async def delete_oga_files(directory='.'):
    for filename in os.listdir(directory):
        if filename.endswith('.oga'):
            os.remove(filename)
            print(f'Файл {filename} удалён')


#
# async def global_chek(a):
#     global check
#     check = a
#     return
apProvider = AlorPy(Config.UserName, Config.RefreshToken)




def risk(symbol):
    # if symbol.upper() in Risck.K380:
    #     return '380000'
    if symbol.upper() in Risck.k470:
        return '700000'
    if symbol.upper() in Risck.k550:
        return '1000000'
    if symbol.upper() in Risck.k590:
        return '1000000'
    if symbol.upper() in Risck.k640:
        return '1100000'
    if symbol.upper() in Risck.k680:
        return '1300000'
    if symbol.upper() in Risck.k800:
        return '1700000'
    if symbol.upper() in Risck.k950:
        return '2000000'
    return '600000'


def decorator_speed(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        rez = func(*args, **kwargs)
        t = datetime.now() - start
        print(f'Скоромть выполнения  - 🚀 {t}')
        return rez
    return wrapper


#разбивает текст на строки с сайт а disclouser , возращает в формате для сообщения в телеграмм
def disclouser(text):
    rez = re.split(r'\d+\. ', text)
    rezult = rez[0]
    for i in rez:
        if ':' in i:
            j = ' '.join(i.split()[:2])
            f = f'📌{j} : {i.split(":")[-1]}\n'
            rezult += f
    return rezult


#проверка поступаещего сообщения на ключевые слова в нем и
async def keyword_check(text, keywords):
    text = [str(i).upper() for i in text.split()]
    keywords = [str(i).upper() for i in keywords]
    for i  in text:
        if i in keywords or i[1:] in keywords or i[:-1] in keywords:
            return True
    return False


#возвращает ключевые слова + тикеры
async def get_keyword(text, keywords):
    text = [str(i).upper() for i in text.split()]
    keywords = [str(i).upper() for i in keywords]
    def func(str):
        str1 = str
        return str in keywords or str in Config.tickers_moex or str1[1:] in Config.tickers_moex
    fitered = list(filter(func, text))
    fitered = set(fitered)
    return fitered


#возвращает список очищенный ключевых слов, очищает все что стоит впереди слова и сзади ,
#если ключевое слово в середине слова , то функция его не найдет , если ключевые слова в тексте
#не найдены , возращает смайлик '🤷‍♂'
def get_keyword_tiker_moex(text, dictionary):
    #text: текст для парсисинга , str
    #keyword: список ключевых слов , которых нужно достать из текста , list
    # Разбиваем текст на слова
    words = text.split()

    # Создаем пустой список для ключевых слов
    keywords = []

    # Проверяем каждое слово на наличие в словаре
    for word in words:
        # Удаляем все символы, кроме букв и цифр
        clean_word = re.sub(r'[^\w]', '', word)
        if clean_word in dictionary:
            keywords.append(clean_word)
    # ddd = []
    # text = str(text)
    # text = text.split()#разбиваем текст н аслова
    # # print(text)
    # for i in text:#перебираем каждое слово из текста
    #     for y in keyword:#берем каждое ключевое слова из заданного спика
    #
    #         rez = i.upper().partition(y)#слово из текста переволим в верхний регистр , метод partition
    #         #находит первое вхождение ключевого слова в начале или вконце и возращает список с найденными или пустым
    #         if rez[1] != '':#если список не  пустой
    #             if rez[1] in ddd:#и этого значения еще нет в списке результатов
    #                 continue#если есть такой уже в списке результатов , начинаем со следующего слова
    #             ddd.append(rez[1])#добавляем в список результатта
    # print(text)
    for i in words:#перебираем текст
        # print(i.upper())
        if i.upper() in Config.dict_keywod_tiker:#проверяем на наличие ключей в словаре с ключевыми словами и занчениями в тикерах
            # print(i.upper())
            if Config.dict_keywod_tiker[i.upper()] in keywords:#если результат есть всловаре результатов
                continue#прерываем иттерацию  и берем следующее слово
            keywords.append(Config.dict_keywod_tiker[i.upper()])#добавляем слово в спиок результатов
    return keywords[0] if len(keywords) >= 1 else '🤷‍♂'#

    # text = [str(i).upper() for i in text.split()[0:7]]
    # def func(str):
    #     str1 = str
    #     return str in Config.tickers_moex or str1[1:] in Config.tickers_moex or  str1[:-1] in Config.tickers_moex
    # fitered = list(filter(func, text))


#проверка id канала или чата поступаещего сообщения на наличие его в списке
async def id_check(id, list):
    if id in list:
        return True
    else:
        return False


#фунекция отправзи запроса chatGPT
def get_chatGPT(text):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Стоставь этот текст другими словами  '{text}'",
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.0
      )
    return response["choices"][0]["text"]


#получаем информацию по позициям
def get_pozicion():
    # print(apProvider.GetPositions(Config.PortfolioStocks, Config.exchange))
    rezult = apProvider.GetPositions(Config.PortfolioStocks, Config.exchange)[0]
    rezult = list(rezult.items())
    str = ''
    for key, value in dict(rezult).items():
        str += f'{key} - {value}\n'
    return str

# get_pozicion()
def get_orders():
    str = ''
    rezult = apProvider.GetOrders(Config.PortfolioStocks, Config.exchange)
    return rezult

#получаем стакан
def get_orderbook(symbol):
    rezult = apProvider.GetOrderBook(Config.exchange,symbol,'MOEX')
    return rezult
    # print(rezult["bids"][3]["price"])
    # return (f'{rezult["bids"][0]["price"]} | {rezult["asks"][0]["price"]}\n{rezult["bids"][1]["price"]} | {rezult["asks"][1]["price"]}\n{rezult["bids"][2]["price"]} | {rezult["asks"][2]["price"]}')
    # for i in rezult['bids']:
    #     print(i)


# получаем обрабатываем портфель
def get_portfolio():
    str = ''
    lis = ['Наличные', 'Используется', 'Открыты', 'Прибыль', 'Процент прибыли', 'Комиссия', 'Изиенения', 'Портфель', 'Доступно']
    rezult  = apProvider.GetMoney(Config.PortfolioStocks, Config.exchange)
    c = 0
    for key, value in rezult.items():
        str += f'{lis[c]} - {value}\n'
        c += 1
    return rezult

# get_portfolio()
# #создать  лимитную заявку
# def create_limit_order(symbol, buy, summ,step_best_price ,portfolio='D78230',exchange='MOEX'):
#     x = "asks" if buy == 'buy' else "bids"
#     lot  = Config.info[symbol]['lotsize']
#     price = get_orderbook(symbol)
#     price = price[x][step_best_price]["price"]
#     print(price)
#     lot = int(int(summ) // (lot * price))
#     print(lot)
#     apProvider.CreateLimitOrder(portfolio ,exchange,symbol,buy, lot,float(price))


#функция формирование цены заявки с учетом шага цены , лотностью инструмента на бирже
def calculate_new_price(step, percent, price, is_increase=True):
    #step - шаг минималльной цены акции
    #percent - процент
    #price - цена
    #is_increase - показатель вычисления процента , либо вверх либо вниз,  + или - % от цены .
    if is_increase:
        new_price = price + (price * percent / 100)
    else:
        new_price = price - (price * percent / 100)
    if step >= 1 :
        return int(round(new_price / step) * step)
    else:
        new_price = round(new_price / step) * step
        new_price = "{:.6f}".format(new_price)
        return new_price


#выставление лиимтной заявки на + ли - на 0.4% от цены текущей
@decorator_speed
def create_limit_order_profit(symbol, buy, summ, step_best_price, portfolio='D78230', exchange='MOEX'):
    x = "bids" if buy == 'buy' else "asks" #продать или купить , в бид или аск заявку
    info = Config.info[symbol]#получаем информацию по инструменту (лотность , название , знаки после запятой и пр.)
    lot = info['lotsize']#со словаря info получаем лоность
    price = get_orderbook(symbol)#получаем стакан
    price = price[x][step_best_price]["price"]#получаем цену в стакане , подставляя бид или аск и позицию стакана где "0" лучшая цена
    print(x)
    # price = price - (price * 0.004) if x == "bids" else price + (price  * 0.004)# продать или купить с люсом в 0.4 %
    # is_increase = x == 'bids'
    print(price)
    lot = int(int(summ) // (lot * price))# получаем сколько можно купить на заданную сумму кратно лотности инструмента
    print(info['minstep'])
    # minstep = len(str(info['minstep'])[2:])#минимальный шаг цены (сколько знаков после запятой или целое число)
    price = calculate_new_price(info['minstep'], 0.4, price, x == 'asks')#int(price) if info['minstep'] == 1 else round(float(price), minstep)#формируем цену соответственно лотности
    print(price)
    apProvider.CreateLimitOrder(portfolio, exchange, symbol, buy, lot, price)# выставляем лимитный ордер


def create_automatic_order(text):
    text = [str(i).upper() for i in  text.split()]
    print(text)
    if 'OТКPЫТИE' in text and 'LONG' in text and 'CPOК' in text and 'ИДEИ:' in text and 'ДO' in text:
        print('long')
    else:
        print('stop')


# нахождение всех ключевых слов из списка в тексте
def keyword_search(text, keywords):
    text = text.upper()
    # print(text)
    if all(keyword.upper() in text for keyword in keywords):
        return True
    else:
        return False


#нахождение любого ключевого слова или словочетания  из списка
@decorator_speed
def search_any_keyword(text, keywords ):
    for i in keywords:
        if i.lower() in text.lower():
            return True
    return False


#находит корни ключеывх слов через re выражения
def search_re(text, keywords , number):
    rez = [i for i in keywords  if re.search(i.lower() , text.lower())]
    print(f'{len(rez)} {rez}')
    return True if len(rez) >= number else False


#информация лб инструменте
def get_symbol(symbol, exchange='MOEX'):
    rezult = apProvider.GetSymbol(exchange, symbol)
    return rezult


#чтец телеграмм и создать кнопок
async def reader_create_button(text, event , message, id_chennal, smiley,chanell_dict_reverse,bot,  **kwargs):
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))
    if tiker == '🤷‍♂':
        markup = InlineKeyboardMarkup()
        # создаем кнопку внизу сообщения с названием "Опубликовать" и id - 'but_1'
        but_1 = InlineKeyboardButton(f'🤷‍♂ Тикер акции MOEX не найден', callback_data=f'2 10000 buy {tiker}')
        markup.add(but_1)
        # редактируем текст сообщениия , добавляем имя канала в переменной chat_name {Config.channel_vip_dict_reverse[id_chennal]
        text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{text}"
        await bot.send_message(-1001701470058, text, reply_markup=markup)
    else:
        key_word = ['идея', '#идея', 'лонг', 'long', 'покупаю',
                    'купил', 'шорт', 'short', 'продаю', 'продал',
                    'покупка', 'открыл', 'взял', 'фиксирую',
                    'зафиксировал', 'фиксируем', 'закрыл', 'закрываю', 'закройте', 'закрываем']
        value = await keyword_check(text, key_word)
        if value:
            key_word_long = ['лонг', 'long', 'покупаю', 'купил', 'покупка', 'взял', 'открыл лонг']
            value = await keyword_check(text, key_word_long)
            if value:
                # tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))
                #создаем клавиатуру
                markup = InlineKeyboardMarkup(row_width=4)
                # создаем кнопку внизу сообщения с названием "Опубликовать" и id - 'but_1'
                but_1 = InlineKeyboardButton(f'🟢{tiker}', callback_data=f'2 0 0 {tiker}')
                but_2 = InlineKeyboardButton(f'200', callback_data=f'0 200000 buy {tiker}')
                but_3 = InlineKeyboardButton(f'80k', callback_data=f'0 80000 buy {tiker}')
                but_4 = InlineKeyboardButton(f'40k', callback_data=f'0 40000 buy {tiker}')
                but_5 = InlineKeyboardButton(f'🔴{tiker}', callback_data=f'2 0 0 {tiker}')
                but_6 = InlineKeyboardButton(f'200', callback_data=f'0 200000 sell {tiker}')
                but_7 = InlineKeyboardButton(f'80k', callback_data=f'0 80000 sell {tiker}')
                but_8 = InlineKeyboardButton(f'40k', callback_data=f'0 40000 sell {tiker}')
                # добавляем кнопку в клавиатуру
                markup.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8)
                # редактируем текст сообщениия , добавляем имя канала в переменной chat_name {Config.channel_vip_dict_reverse[id_chennal]
                text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{text}"
                # print('long')
                # отправка сообщения ботом в канал с клавиатурой
                await bot.send_message(-1001701470058, text, reply_markup=markup)
                # print(f'{"Покупка"} : {tiker}')
            key_word_short = ['шорт', 'short', 'продаю', 'продал', 'закрыл лонг', 'фиксирую',
                              'зафиксировал', 'фиксируем', 'закрыл', 'закрываю', 'закройте',
                              'закрываем']
            value =await keyword_check(text, key_word_short)
            # print(value)
            if value:
                # tiker= str(get_keyword_tiker_moex(text, Config.tickers_moex))
                # создаем клавиатуру
                markup = InlineKeyboardMarkup(row_width=4)
                # создаем кнопку внизу сообщения с названием "Опубликовать" и id - 'but_1'
                but_1 = InlineKeyboardButton(f'🔴{tiker}', callback_data=f'2 0 0 {tiker}')
                but_2 = InlineKeyboardButton(f'200', callback_data=f'0 200000 sell {tiker}')
                but_3 = InlineKeyboardButton(f'80k', callback_data=f'0 80000 sell {tiker}')
                but_4 = InlineKeyboardButton(f'40k', callback_data=f'0 40000 sell {tiker}')
                but_5 = InlineKeyboardButton(f'🟢{tiker}', callback_data=f'2 0 0 {tiker}')
                but_6 = InlineKeyboardButton(f'200', callback_data=f'0 200000 buy {tiker}')
                but_7 = InlineKeyboardButton(f'80k', callback_data=f'0 80000 buy {tiker}')
                but_8 = InlineKeyboardButton(f'40k', callback_data=f'0 40000 buy {tiker}')
                # добавляем кнопку в клавиатуру
                markup.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8)
                print('short')
                # редактируем текст сообщениия , добавляем имя канала в переменной chat_name {Config.channel_vip_dict_reverse[id_chennal]
                text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{text}"
                # отправка сообщения ботом в канал с клавиатурой
                await bot.send_message(-1001701470058, text, reply_markup=markup)
        else:
            # tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))
            # создаем клавиатуру
            markup = InlineKeyboardMarkup(row_width=4)
            # создаем кнопку внизу сообщения с названием "Опубликовать" и id - 'but_1'
            but_1 = InlineKeyboardButton(f'🟢{tiker}', callback_data=f'2 0 0 {tiker}')
            but_2 = InlineKeyboardButton(f'200', callback_data=f'0 200000 buy {tiker}')
            but_3 = InlineKeyboardButton(f'80k', callback_data=f'0 80000 buy {tiker}')
            but_4 = InlineKeyboardButton(f'40k', callback_data=f'0 40000 buy {tiker}')
            but_5 = InlineKeyboardButton(f'🔴{tiker}', callback_data=f'2 0 0 {tiker}')
            but_6 = InlineKeyboardButton(f'200', callback_data=f'0 200000 sell {tiker}')
            but_7 = InlineKeyboardButton(f'80k', callback_data=f'0 80000 sell {tiker}')
            but_8 = InlineKeyboardButton(f'40k', callback_data=f'0 40000 sell {tiker}')
            # добавляем кнопку в клавиатуру
            markup.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8)
            # редактируем текст сообщениия , добавляем имя канала в переменной chat_name {Config.channel_vip_dict_reverse[id_chennal]
            text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{text}"
            # print('long')
            # отправка сообщения ботом в канал с клавиатурой
            await bot.send_message(-1001701470058, text, reply_markup=markup)


import concurrent.futures


def get_price(symbol, x, step_best_price):
    #symbol = тикер
    #x = bids или asks
    #step_best_price = шаг цены в стакане, где [0] - лучшая цена в стакане и далее по всей глубине стакана
    price = get_orderbook(symbol)
    return price[x][step_best_price]["price"]

@decorator_speed
def create_limit_order(symbol, buy, summ, step_best_price, portfolio='D78230', exchange='MOEX'):
    x = "asks" if buy == 'buy' else "bids"
    info = Config.info[symbol]
    lot = info['lotsize']
    minstep = info['minstep']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        price_future = executor.submit(get_price, symbol, x, step_best_price)
        price = price_future.result()
        lot = int(int(summ) // (lot * price))
        # price = calculate_new_price(info['minstep'], 0.4, price, x == 'asks')
        if minstep >= 1:
            apProvider.CreateLimitOrder(portfolio, exchange, symbol, buy, lot, int(price))
            print(f'Цена покупки int {int(price)}')
            print(lot)
        else:
            apProvider.CreateLimitOrder(portfolio, exchange, symbol, buy, lot, float(price))
            print(f'Цена покупки float {float(price)}')
            print(lot)


def get_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers)
    return response




async def convert_audio_text(event, client):
    if event.message.voice:
        voice_message = event.message.voice
        # Скачиваем голосовое сообщение
        voice_data = await client.download_file(voice_message)
        with open('voice_message.ogg', 'wb') as f:
            f.write(voice_data)
        convert_ogg_wav('voice_message.ogg')
        if voice_data:
            print('ПРеобразую звук в текст')
            audiotext = audio_to_text('voice_message.wav')
            return audiotext
    else:
        print('В данном сообщении голосового не обнаружено')
        return None




 #функция нажатия инлайн кнопки и возврата текста который должен появиться по нажатию кнопки
async def nazatie_knopki(event, client, types, events):
    #event - необработанное сообщение
    #client - клиент телеграмм
    #types - модуль  telethon
    #events - модуль  telethon
    if event.message.reply_markup and event.message.reply_markup.rows:
        inline_button = event.message.reply_markup.rows[0].buttons[0]
        if isinstance(inline_button, types.KeyboardButtonCallback):
            await client.send_callback_query(event.chat_id, event.message.id, data=inline_button.data)
            response_message = await client.listen(events.NewMessage(incoming=True, from_users=event.sender_id))
            text = response_message.message
            return text