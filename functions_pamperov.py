import sqlite3
import asyncio
from all_functions import keyword_search, risk, create_limit_order, search_any_keyword, search_re, get_price
from keywords import Keywords, Risck
from Config import Config
import re



mosinvestor_flag = True
fibo_flag = True
cashflou_public_flag = True
unique_flag = True
goodwin_flag = True
venividivici_vip_flag = True
oleg_flag = True


def start_stop_db(id  = None, column ='start_stop', name_table ='statr_stop_zakupki'):
    with sqlite3.connect('my_database.db') as conn:
        # Создание объекта курсора, который будет выполнять SQL-запросы
        cursor = conn.cursor()
        if id is not None:
            # Выполнение запроса SELECT для получения всех записей из таблицы
            cursor.execute(f"SELECT {column} FROM {name_table} WHERE name_chenal = '{id}'")
            # Получение всех записей из таблицы
            row = cursor.fetchall()
            return row[0]
        else:
            cursor.execute(f"SELECT {column} FROM {name_table}")
            # Получение всех записей из таблицы
            row = cursor.fetchall()
            return row


async def oleg_reading(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('oleg_public')):
        keyword_Oleg1 = ['#ИДЕЯ', 'ЛОНГ', 'ВХОД']
        keyword_Oleg2 = ['ИДЕЯ', 'ЛОНГ', 'ВХОД']
        stop = ['GMKN', 'RUAL', 'SBER', 'GAZP', 'LKOH']
        if tiker not in stop:
            if keyword_search(text, keyword_Oleg1) or keyword_search(text, keyword_Oleg2):
                print('long - 👉 🎈Олег торгует')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker,'asks',1)
        text2 = f"👉 Сигнал 🎈Олег торгует \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала K-traide
async def k_trade_reading(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('k_trade')):
        keyword_KTrade = ['ЛОНГ', 'ВХОД:']
        keyword_KTrade1 = ['ЗАХОДИМ', 'СПЕКУЛЯТИВНО']
        keyword_KTrade2 = ['МОЖНО', 'ЗАЙТИ']
        keyword_KTrade3 = ['МОЖНО', 'ВЗЯТЬ']
        if keyword_search(text, keyword_KTrade) or keyword_search(text, keyword_KTrade1) or keyword_search(text,keyword_KTrade2) or keyword_search(text, keyword_KTrade3):
            print('long - 👉 🎈K - trade ')
            create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈K - trade \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)



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
async def goodwin_reading(text,tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    keyword_Goodwin1 = ['Покупка', 'Стоп' , 'Профит' ]
    if bool(*start_stop_db('goodwin_vip')):
        if re.search('#скальпин',text, 1) or re.search('#срeднeсрок',text, 1):
            if keyword_search(text, keyword_Goodwin1):
                print('long - 👉 🎈Goodwin Production')
                create_limit_order(tiker, buy, summ, 1)
            # else:
            #     if search_re(text,Keywords.goodwin_short, 1):
            #         print('🤬')
            #     else:
            #         if search_any_keyword(text, Keywords.goodwin) or search_re(text,Keywords.goodwin2, 2):
            #             buy = 'buy'
            #             summ = risk(tiker)
            #             print('long - 👉 🎈Goodwin Production')
            #             create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker,'asks', 1)
        text2 = f"👉 Сигнал 🎈Goodwin Production \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала Чехов вип
async def chehov_reading(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('chehov_vip')):
        if search_any_keyword(text, Keywords.chehov_short):
            print('stop -  👉 🎈Чехов ВИП канал')
        else:
            keyword1 = ['ПРИКУПИТЕ', 'НЕМНОГО']
            keyword2 = ['ПРИКУПИМ', 'НЕМНОГО']
            keyword3 = ['ПОКУПАЕМ', 'НЕМНОГО']
            keyword4 = ['ПОКУПАЮ', 'НЕМНОГО']
            if keyword_search(text, keyword1) or keyword_search(text, keyword2) or keyword_search(text,keyword3) or keyword_search(text, keyword4) or search_any_keyword(text, Keywords.chehov):
                print('long - 👉 🎈Чехов ВИП канал')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈Чехов ВИП канал \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)



#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала ProfitKing
async def ProfitKing_reading(text,tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('profit_king_vip')):
        keyword1 = ['КУПИЛ']
        keyword2 = ['ПОКУПКА']
        keyword3 = ['ВЗЯЛ']
        keyword4 = ['ПОКУПАЮ']
        keyword5 = ['ПЕРЕЗАХОЖУ']
        stop = 'Россети'
        if stop.upper() not in text.upper():
            if tiker in Config.rts2_3 and tiker not in Risck.blu_tikers:
                if len(str(text).split()) <= 12 and keyword_search(text, keyword5) or keyword_search(text,keyword2) or keyword_search(text, keyword3) or keyword_search(text, keyword4) or keyword_search(text, keyword1):
                    print('long - 👉 🎈Клуб ProfitKing')
                    create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈Клуб ProfitKing \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала Биржевик
async def birgewik_reading(text,tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('birgevik_vip')):
        keyword1 = ['цель', 'средняя', 'лонг']
        keyword4 = ['⚡️Беру', 'беру', '⚡️Забираю']
        stop = ['GMKN', 'шорт', 'SBER', 'GAZP']
        if tiker not in stop:
            if search_any_keyword(text,Keywords.birgewik) and search_any_keyword(text,keyword1):
                print('long 👉 🎈Биржевик | VipPirates')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈Биржевик | VipPirates \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)


# обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала Черных мастер
async def chernihMaster_reading(text,tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('chernihMaster_vip')):
        if search_re(text,Keywords.chernih_short, 1 ):
            print('stop 👉 🎈Черных мастер Россия')
        else:
            keyword4 = ['Покупаю', 'Куплю', 'Открываю лонг']
            keyword5 = ['лонг', 'тeкущeй ']
            keyword6 = ['лонг', 'текущей' , 'цене']
            if search_any_keyword(text, keyword4) or keyword_search(text, keyword5) or keyword_search(text,keyword6):
                print('long 👉 🎈Черных мастер Россия')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈Черных мастер Россия \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)


#обработка сообщений по ключевым словам и выставление лимитной заявки для сообщений какнала cashflow публичный
async def cashflow_publick_reading(text,tiker, bot ):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('cashflou_public')):
        keyword4 = ['ПОКУПКА ЛОНГ!', 'ВХОД:']
        keyword5 = ['ПОКУПКА LONG!', 'ВХОД:']
        if tiker in Config.rts2_3 and tiker not in Risck.blu_tikers:
            if keyword_search(text, keyword4) or keyword_search(text, keyword5):
                print('long 👉 🎈СИГНАЛЫ от CASHFLOW')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈СИГНАЛЫ от CASHFLOW publik \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)



async def mosinvestor_publick_reading(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('masinvestor')):
        keyword4 = ['🚨Покупка', '🪙Цена:', '🏆Выход:']
        if tiker in Config.rts2_3 and tiker not in Risck.blu_tikers:
            if keyword_search(text, keyword4):
                print('long 👉 🎈СИГНАЛЫ МОСКОВСКИЙ ИНВЕСТОР')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈СИГНАЛЫ МОСКОВСКИЙ ИНВЕСТОР \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)


async def unique_trade(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('unique_public')):
        keyword4 = ['КУПИЛ', 'ЛОНГ', 'Вход']
        keyword5 = ['КУПИЛ', 'Вход']
        # stop = ['GMKN', 'NMTP']
        # if tiker not in stop:
        if tiker in Config.rts2_3 and tiker not in Risck.blu_tikers:
            if keyword_search(text, keyword4) or keyword_search(text, keyword5) :
                print('long 👉 🎈UNIQUE TRADE 🐥')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈UNIQUE TRADE 🐥 \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)


async def cashflow_vip_reading(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('cashflow_vip')):
        keyword4 = ['ПОКУПКА ЛОНГ!', 'ВХОД:']
        keyword5 = ['ПОКУПКА LONG!', 'ВХОД:']
        if tiker in Config.rts2_3 and tiker not in Risck.blu_tikers:
            if keyword_search(text, keyword4) or keyword_search(text, keyword5):
                if keyword_search(text, keyword4):
                    # summ = '100000'
                    print('long 👉 🎈СИГНАЛЫ от CASHFLOW')
                    create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈СИГНАЛЫ от CASHFLOW vip \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)



async def kogan_vip_reading(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('kogan_vip')):
        keyword4 = ['⚡️Покупаем', '#push']
        keyword5 = ['⚡️Докупаем', '#push']
        if keyword_search(text, keyword4) or keyword_search(text, keyword5) :
            # summ = '100000'
            print('long 👉 🎈Kogan vip')
            create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈Kogan vip \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)



async def venividivici_vip_reading(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('venividivici_vip')):
        keyword4 = ['buy:', 'sl:', 'tp:']
        if tiker in Config.rts2_3 and tiker not in Risck.blu_tikers:
            if keyword_search(text, keyword4):
                # summ = '100000'
                print('long 👉 🎈venividivici')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈Venividivici vip \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)


async def fibo_vip(text, tiker, bot):
    buy = 'buy'
    summ = risk(tiker)
    if bool(*start_stop_db('fibo_vip')):
        keyword4 = ['Покупка:', 'Цель: ']
        if tiker in Config.rts2_3 and tiker not in Risck.blu_tikers:
            if keyword_search(text, keyword4):
                # summ = '200000'
                print('long 👉 🎈fibo_vip')
                create_limit_order(tiker, buy, summ, 1)
    else:
        price = get_price(tiker, 'asks', 1)
        text2 = f"👉 Сигнал 🎈Fibo_vip \n👉 Закупка выключена\n👉 Можно было купить {tiker} по - {price}"
        await bot.send_message(-1001701470058, text2)

# print(bool(*start_stop_db('unique_public')))