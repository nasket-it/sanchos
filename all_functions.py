from main import bot, client
from AlorPy import AlorPy  # Работа с Alor OpenAPI V2
from Config import *
import openai
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import time
from datetime import datetime



#
# async def global_chek(a):
#     global check
#     check = a
#     return
apProvider = AlorPy(Config.UserName, Config.RefreshToken)


def decorator_speed(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        rez = func(*args, **kwargs)
        t = datetime.now() - start
        print(f'Скоромть выполнения - 🚀 {t}')
        return rez
    return wrapper





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
    rezult = apProvider.GetPositions(Config.PortfolioStocks, Config.exchange)[0]
    rezult = list(rezult.items())[:3]
    str = ''
    for key, value in dict(rezult).items():
        str += f'{key} - {value}\n'
    return str


def get_orders():
    str = ''
    rezult = apProvider.GetOrders(Config.PortfolioStocks, Config.exchange)
    return rezult


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
    if step == 1 :
        return round(new_price / step) * step
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
    text = [str(i).upper() for i in text.split()]
    # print(text)
    if all(keyword in text for keyword in keywords):
        return True
    else:
        return False




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
                markup = InlineKeyboardMarkup(row_width=3)
                # создаем кнопку внизу сообщения с названием "Опубликовать" и id - 'but_1'
                but_1 = InlineKeyboardButton(f'🟢{tiker} 40k', callback_data=f'0 40000 buy {tiker}')
                but_2 = InlineKeyboardButton(f'🟢{tiker} 80k', callback_data=f'0 80000 buy {tiker}')
                but_3 = InlineKeyboardButton(f'🔴 +0,4% 40k', callback_data=f'1 40000 sell {tiker}')
                but_4 = InlineKeyboardButton(f'🔴{tiker} 40k', callback_data=f'0 40000 sell {tiker}')
                but_5 = InlineKeyboardButton(f'🔴{tiker} 80k', callback_data=f'0 80000 sell {tiker}')
                but_6 = InlineKeyboardButton(f'🟢 -0,4% 40k', callback_data=f'1 40000 buy {tiker}')
                # добавляем кнопку в клавиатуру
                markup.add(but_1, but_2, but_3, but_4, but_5, but_6)
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
                markup = InlineKeyboardMarkup(row_width=3)
                # создаем кнопку внизу сообщения с названием "Опубликовать" и id - 'but_1'
                but_1 = InlineKeyboardButton(f'🔴{tiker} 40k', callback_data=f'0 40000 sell {tiker}')
                but_2 = InlineKeyboardButton(f'🔴{tiker} 80k', callback_data=f'0 80000 sell {tiker}')
                but_3 = InlineKeyboardButton(f'🟢 -0,4% 40k', callback_data=f'1 40000 buy {tiker}')
                but_4 = InlineKeyboardButton(f'🟢{tiker} 40k', callback_data=f'0 40000 buy {tiker}')
                but_5 = InlineKeyboardButton(f'🟢{tiker} 80k', callback_data=f'0 80000 buy {tiker}')
                but_6 = InlineKeyboardButton(f'🔴 +0,4% 40k', callback_data=f'1 40000 sell {tiker}')
                # добавляем кнопку в клавиатуру
                markup.add(but_1, but_2, but_3, but_4, but_5, but_6)
                print('short')
                # редактируем текст сообщениия , добавляем имя канала в переменной chat_name {Config.channel_vip_dict_reverse[id_chennal]
                event.message.text = f'{smiley}\n\n{chanell_dict_reverse[id_chennal]}' + f"\n\n{event.message.text}"
                # отправка сообщения ботом в канал с клавиатурой
                await bot.send_message(-1001701470058, message.message, reply_markup=markup)
        else:
            # tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))
            # создаем клавиатуру
            markup = InlineKeyboardMarkup(row_width=3)
            # создаем кнопку внизу сообщения с названием "Опубликовать" и id - 'but_1'
            but_1 = InlineKeyboardButton(f'🟢{tiker} 40k', callback_data=f'0 40000 buy {tiker}')
            but_2 = InlineKeyboardButton(f'🟢{tiker} 80k', callback_data=f'0 80000 buy {tiker}')
            but_3 = InlineKeyboardButton(f'🔴 +0,4% 40k', callback_data=f'1 40000 sell {tiker}')
            but_4 = InlineKeyboardButton(f'🔴{tiker} 40k', callback_data=f'0 40000 sell {tiker}')
            but_5 = InlineKeyboardButton(f'🔴{tiker} 80k', callback_data=f'0 80000 sell {tiker}')
            but_6 = InlineKeyboardButton(f'🟢 -0,4% 40k', callback_data=f'1 400000 buy {tiker}')
            # добавляем кнопку в клавиатуру
            markup.add(but_1, but_2, but_3, but_4, but_5, but_6)
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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        price_future = executor.submit(get_price, symbol, x, step_best_price)
        price = price_future.result()

        lot = int(int(summ) // (lot * price))
        # price = calculate_new_price(info['minstep'], 0.4, price, x == 'asks')

        apProvider.CreateLimitOrder(portfolio, exchange, symbol, buy, lot, float(price))

    # rezult_ison = []
    # all_potok_futures = []
    # def fanc(tikers, str1=str):
    #     try:
    #         rezult_ison.append(get_tiker(tikers, str1))
    #     except:
    #         rezult_ison.append('0')
    # for i in list_tikers: # проходим цыклом по словярю с тикерами фьючерсов
    #     pt_1 = threading.Thread(target=fanc, args=(i,str)) #создаем поток функции гет запроса
    #     all_potok_futures.append(pt_1) #добавляем все потоки запросов в список всех потокот , чтобы не ждать
    #     pt_1.start()  #запускаем каждый поток
    # for i in all_potok_futures:# запускаем цыкл по списку всех потоков программы
    #     i.join() # ждем пока все потоки завершаться
    # return rezult_ison









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

# Использование функции
source_channel = 'source_channel_id'
destination_channel = 'destination_channel_id'
time_interval = 24 * 60 * 60  # 24 часа (в секундах)
delay = 5  # Задержка в 5 секунд между отправкой каждого сообщения


# loop = asyncio.get_event_loop()
# loop.run_until_complete(forward_messages(source_channel, destination_channel, time_interval, delay))
# print(get_symbol("MOEX")['lotsize'])

# rez = get_symbol('SBER')
# print(rez['lotsize'])
# get_symbol('SBER')
# create_limit_order('gazp')
#
# get_orderbook('SBER')

# apProvider.CreateLimitOrder('D78230','MOEX', 'GAZP', 'buy', 1, 179.03)