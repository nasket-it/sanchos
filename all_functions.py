from numba import njit
from main import bot, client
from AlorPy import AlorPy  # Работа с Alor OpenAPI V2
from Config import *
from keywords import Keywords, Risck
import openai
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import time
import re
from datetime import datetime
import requests



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
        return '520000'
    if symbol.upper() in Risck.k550:
        return '620000'
    if symbol.upper() in Risck.k590:
        return '680000'
    if symbol.upper() in Risck.k640:
        return '720000'
    if symbol.upper() in Risck.k680:
        return '780000'
    if symbol.upper() in Risck.k800:
        return '900000'
    if symbol.upper() in Risck.k950:
        return '1000000'
    return '400000'


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
def get_keyword_tiker_moex(text, keyword):
    #text: текст для парсисинга , str
    #keyword: список ключевых слов , которых нужно достать из текста , list
    ddd = []
    text = str(text)
    text = text.split()#разбиваем текст н аслова
    # print(text)
    for i in text:#перебираем каждое слово из текста
        for y in keyword:#берем каждое ключевое слова из заданного спика
            rez = i.upper().partition(y)#слово из текста переволим в верхний регистр , метод partition
            #находит первое вхождение ключевого слова в начале или вконце и возращает список с найденными или пустым
            if rez[1] != '':#если список не  пустой
                if rez[1] in ddd:#и этого значения еще нет в списке результатов
                    continue#если есть такой уже в списке результатов , начинаем со следующего слова
                ddd.append(rez[1])#добавляем в список результатта
    # print(text)
    for i in text:#перебираем текст
        # print(i.upper())
        if i.upper() in Config.dict_keywod_tiker:#проверяем на наличие ключей в словаре с ключевыми словами и занчениями в тикерах
            # print(i.upper())
            if Config.dict_keywod_tiker[i.upper()] in ddd:#если результат есть всловаре результатов
                continue#прерываем иттерацию  и берем следующее слово
            ddd.append(Config.dict_keywod_tiker[i.upper()])#добавляем слово в спиок результатов
    return ddd[0] if len(ddd) >= 1 else '🤷‍♂'#

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
    return str


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
    # decimal_part = str(price).split('.')[1]
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
async def reader_create_button(text, event , message, id_chennal, smiley,chanell_dict_reverse, **kwargs):
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))
    if tiker == '🤷‍♂':
        markup = InlineKeyboardMarkup()
        # создаем кнопку внизу сообщения с названием "Опубликовать" и id - 'but_1'
        but_1 = InlineKeyboardButton(f'🤷‍♂ Тикер акции MOEX не найден', callback_data=f'2 10000 buy {tiker}')
        markup.add(but_1)
        # редактируем текст сообщениия , добавляем имя канала в переменной chat_name {Config.channel_vip_dict_reverse[id_chennal]
        event.message.text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{event.message.text}"
        await bot.send_message(-1001701470058, message.message, reply_markup=markup)
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
                event.message.text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{event.message.text}"
                # print('long')
                # отправка сообщения ботом в канал с клавиатурой
                await bot.send_message(-1001701470058, message.message, reply_markup=markup)
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
                event.message.text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{event.message.text}"
                # отправка сообщения ботом в канал с клавиатурой
                await bot.send_message(-1001701470058, message.message, reply_markup=markup)
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
            event.message.text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{event.message.text}"
            # print('long')
            # отправка сообщения ботом в канал с клавиатурой
            await bot.send_message(-1001701470058, message.message, reply_markup=markup)


import concurrent.futures


def get_price(symbol, x, step_best_price):
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


async def forward_messages(source_channel, destination_channel, time_interval, delay):
    # Определение временных границ для получения истории сообщений
    until_date = None
    if time_interval > 0:
        until_date = int(time.time())  # Текущая дата и время в Unix-формате
        from_date = until_date - time_interval

    # Получение истории сообщений канала за указанный временной интервал
    async for message in client.iter_messages(source_channel, limit=10, reverse=True, from_user='me'):
        # Задержка перед пересылкой сообщения в другой канал
        # await asyncio.sleep(delay)
        print(message)
        # Пересылка сообщения в другой канал
        # await client.forward_messages(destination_channel, message)

#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала Олег торгуе
def oleg_reading(text, tiker):
    keyword_Oleg1 = ['#ИДЕЯ', 'ЛОНГ', 'ВХОД']
    keyword_Oleg2 = ['ИДЕЯ', 'ЛОНГ', 'ВХОД']
    stop = ['GMKN', 'RUAL', 'SBER', 'GAZP', 'LKOH']
    if tiker not in stop:
        if keyword_search(text, keyword_Oleg1) or keyword_search(text, keyword_Oleg2):
            buy = 'buy'
            summ = risk(tiker)
            print('long - 👉 🎈Олег торгует')
            create_limit_order(tiker, buy, summ, 1)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала K-traide
def k_trade_reading(text, tiker):
    keyword_KTrade = ['ЛОНГ', 'ВХОД:']
    keyword_KTrade1 = ['ЗАХОДИМ', 'СПЕКУЛЯТИВНО']
    keyword_KTrade2 = ['МОЖНО', 'ЗАЙТИ']
    keyword_KTrade3 = ['МОЖНО', 'ВЗЯТЬ']
    if keyword_search(text, keyword_KTrade) or keyword_search(text, keyword_KTrade1) or keyword_search(text,keyword_KTrade2) or keyword_search(text, keyword_KTrade3):
        buy = 'buy'
        summ = risk(tiker)
        print('long - 👉 🎈K - trade ')
        create_limit_order(tiker, buy, summ, 1)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала RDV - премиум
def RDV_reading(text,tiker):
    keyword_RDV = ['OТКPЫТИE', 'LONG', 'CPOК', 'ИДEИ:',
                   'ДO']  # ключевые слова на покупку сигнала из сообщений этого канала
    if keyword_search(text, keyword_RDV):  # если в тексте сообщения есть ВСЕ!!! слова ключевые
        buy = 'buy'  # покупаем или продаем , настраивается вручную
        summ = '100000'  # сумма покупки , насраивается вручную
        print('long - 👉 🎈РДВ Premium')
        # create_limit_order(tiker, buy, summ, 1)  # функция покупки


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала Goodwin
def goodwin_reading(text,tiker):
    keyword_Goodwin1 = ['Покупка', 'Стоп' , 'Профит' ]
    if re.search('#скальпин',text, 1):
        if keyword_search(text, keyword_Goodwin1):
            buy = 'buy'
            summ = risk(tiker)
            print('long - 👉 🎈Goodwin Production')
            create_limit_order(tiker, buy, summ, 1)
        else:
            if search_re(text,Keywords.goodwin_short, 1):
                print('🤬')
            else:
                if search_any_keyword(text, Keywords.goodwin) or search_re(text,Keywords.goodwin2, 2):
                    buy = 'buy'
                    summ = risk(tiker)
                    print('long - 👉 🎈Goodwin Production')
                    create_limit_order(tiker, buy, summ, 1)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала Чехов вип
def chehov_reading(text, tiker):
    if search_any_keyword(text, Keywords.chehov_short):
        print('stop -  👉 🎈Чехов ВИП канал')
    else:
        keyword1 = ['ПРИКУПИТЕ', 'НЕМНОГО']
        keyword2 = ['ПРИКУПИМ', 'НЕМНОГО']
        keyword3 = ['ПОКУПАЕМ', 'НЕМНОГО']
        keyword4 = ['ПОКУПАЮ', 'НЕМНОГО']
        if keyword_search(text, keyword1) or keyword_search(text, keyword2) or keyword_search(text,keyword3) or keyword_search(text, keyword4) or search_any_keyword(text, Keywords.chehov):
            buy = 'buy'
            summ = risk(tiker)
            print('long - 👉 🎈Чехов ВИП канал')
            create_limit_order(tiker, buy, summ, 1)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала ProfitKing
def ProfitKing_reading(text,tiker):
    keyword1 = ['КУПИЛ']
    keyword2 = ['ПОКУПКА']
    keyword3 = ['ВЗЯЛ']
    keyword4 = ['ПОКУПАЮ']
    keyword5 = ['ПЕРЕЗАХОЖУ']
    if len(str(text).split()) <= 12 and keyword_search(text, keyword5) or keyword_search(text,keyword2) or keyword_search(text, keyword3) or keyword_search(text, keyword4) or keyword_search(text, keyword1):
        buy = 'buy'
        summ = risk(tiker)
        print('long - 👉 🎈Клуб ProfitKing')
        create_limit_order(tiker, buy, summ, 1)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала Биржевик
def birgewik_reading(text,tiker):
    keyword1 = ['цель', 'средняя', 'лонг']
    keyword4 = ['⚡️Беру', 'беру', '⚡️Забираю']
    stop = ['GMKN', 'шорт', 'SBER', 'GAZP']
    if tiker not in stop:
        if search_any_keyword(text,Keywords.birgewik) and search_any_keyword(text,keyword1):
            buy = 'buy'
            summ = risk(tiker)
            print('long 👉 🎈Биржевик | VipPirates')
            create_limit_order(tiker, buy, summ, 1)


# обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала Черных мастер
def chernihMaster_reading(text,tiker):
    keywords1 = ['не покупаю' , 'не куплю']
    if search_any_keyword(text,keywords1 ):
        print('stop 👉 🎈Черных мастер Россия')
    else:
        keyword4 = ['Покупаю', 'Куплю', 'Открываю лонг']
        keyword5 = ['лонг', 'тeкущeй ']
        if search_any_keyword(text, keyword4) or keyword_search(text, keyword5) :
            buy = 'buy'
            summ = risk(tiker)
            print('long 👉 🎈Черных мастер Россия')
            create_limit_order(tiker, buy, summ, 1)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала cashflow публичный
def cashflow_publick_reading(text,tiker):
    keyword4 = ['ПОКУПКА ЛОНГ!', 'ВХОД:']
    if search_any_keyword(text, keyword4):
        buy = 'buy'
        summ = risk(tiker)
        print('long 👉 🎈СИГНАЛЫ от CASHFLOW')
        create_limit_order(tiker, buy, summ, 1)



def mosinvestor_publick_reading(text,tiker):
    keyword4 = ['🚨Покупка', '🪙Цена:', '🏆Выход:']
    if tiker in Config.rts2_3:
        if search_any_keyword(text, keyword4):
            buy = 'buy'
            summ = risk(tiker)
            print('long 👉 🎈СИГНАЛЫ МОСКОВСКИЙ ИНВЕСТОР')
            create_limit_order(tiker, buy, summ, 1)

def cashflow_vip_reading(text,tiker):
    keyword4 = ['ПОКУПКА ЛОНГ!', 'ВХОД:']
    if tiker in Config.rts2_3:
        if search_any_keyword(text, keyword4):
            buy = 'buy'
            summ = risk(tiker)
            # summ = '100000'
            print('long 👉 🎈СИГНАЛЫ от CASHFLOW')
            create_limit_order(tiker, buy, summ, 1)