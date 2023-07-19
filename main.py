from secrete import Token
# from message_reading import oleg_reading
from telethon import *
from all_functions import *
from aiogram import Bot, Dispatcher , types, executor

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
# from AlorPy import AlorPy  # Работа с Alor OpenAPI V2
from keywords import Keywords, Risck
from Config import Config  # Файл конфигурации
from bs4 import BeautifulSoup


API_TOKEN = Token.bot_token


# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


#создаем клиента на Алор
# apProvider = AlorPy(Config.UserName, Config.RefreshToken)

exchange = 'MOEX'  # Код биржи MOEX или SPBX
symbol = 'SBER'  # Тикер
port_io = 'D78230'


#api ключи и токены
account = ['-1001892817733','-1001857334624']
api_id = Token.api_id  # задаем API
api_hash = Token.api_hash  # задаем HASH
phone = Token.phone



client = TelegramClient('my_account.session', api_id, api_hash)



#в этой переменной храниться последнее сообщение отправленное в канал новостоной
#перед отправкой следующего сообщения проверяется текст этого , для предотращения дублей
check1 = 0
all_signals = []

async def get_dialodgs():
    dialogs = await client.get_dialogs()
    dialogs = [f'{i.name} : {i.id}' for i in dialogs ]
    print(dialogs)


#получаем все диалоги , функция корутина (запускается в самом низу листа )


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Привет')\

@dp.message_handler()
async def process_start_command(message: types.Message):
    print(message)
    url = message["entities"][0]["url"]
    print(url)
    response = get_request(url)
    soup = BeautifulSoup(response.text , 'html.parser')
    div_tag = soup.find('div', {'style': 'word-break: break-word; word-wrap: break-word; white-space: pre-wrap;'})
    if div_tag:
        extracted_text = div_tag.get_text(strip=True)
        text = disclouser(extracted_text)
        print(extracted_text)
        print(text)
    # await bot.send_message(message.chat.id, 'Привет')




#щбработчик нажатия инлайн кнопок
@dp.callback_query_handler()
async def buttons_press(callback_query):
    print(callback_query.data)
    if str(callback_query.data).split()[0] == '2':
        tiker = str(callback_query.data).split()[-1]
        print(tiker)
        buy = 'buy'
        print(buy)
        summ = risk(tiker)
        create_limit_order(tiker, buy, summ, 0)
        await bot.send_message(-1001701470058,f'😱 full  - {tiker} {summ} {buy} ')
        await callback_query.answer()
    else:
        if str(callback_query.data).split()[0] == '0':
            tiker = str(callback_query.data).split()[-1]
            print(tiker)
            buy = str(callback_query.data).split()[2]
            print(buy)
            summ = str(callback_query.data).split()[1]
            print(summ)
            create_limit_order(tiker,buy,summ, 0)
            await bot.send_message(-1001701470058, f'{tiker}')
            # await bot.send_message(-1001701470058, f'💵Портфель\n{porfolio}\n🧰Позиции\n{pozicion}\n📒Ордера\n{all_orders}')
            await callback_query.answer()
        elif str(callback_query.data).split()[0] == '1':
            tiker = str(callback_query.data).split()[-1]
            print(tiker)
            buy = str(callback_query.data).split()[2]
            print(buy)
            summ = str(callback_query.data).split()[1]
            print(summ)
            create_limit_order_profit(tiker, buy, summ, 0)
            await bot.send_message(-1001701470058, f'{tiker}')
            # await bot.send_message(-1001701470058, f'💵Портфель\n{porfolio}\n🧰Позиции\n{pozicion}\n📒Ордера\n{all_orders}')
            await callback_query.answer()


#обработка сообщений из каналов куплленных и пересылов со списка папперов Config.pamper_channels_id
@client.on(events.NewMessage(chats=Config.pamper_channels_id))
async def pamper_channels_handler(event):
    id_chennal = event.message.chat_id# достаем idчата или какнал от которо пришло сообщение
    text = event.message.message # достаем только текст сообщени
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))# находим тикер в тексте
    if tiker == '🤷‍♂': #если в тексте нет тикера MOEX
        print(f'В данном тексте не обнаружены текеры MOEX')
    else:#если есть тикер в тексте
        # если сообщение от канала РДВ Premium | SS PRO
        # if id_chennal == Config.pamper_channels['РДВ Premium | SS PRO']:
        #     RDV_reading(text, tiker)
        # # если сообщение от канала K-Trade | SS Exclusive'
        # if id_chennal == Config.pamper_channels['K - trade']:
        #     k_trade_reading(text, tiker)
        # # если сообщение от канала Олег торгует
        # if id_chennal == Config.pamper_channels['Олег торгует']:
        #     oleg_reading(text, tiker)
        # если сообщение от канала Goodwin Production |GP Fund | 💎 | SS PRO Exclusive
        # if id_chennal == Config.pamper_channels['Goodwin Production |GP Fund | 💎 | SS PRO Exclusive']:
        #     goodwin_reading(text, tiker)
        # if id_chennal == Config.pamper_channels['Чехов ВИП канал']:
        #     chehov_reading(text, tiker)
        # if id_chennal == Config.pamper_channels['Клуб ProfitKing']:
        #     ProfitKing_reading(text, tiker)
        if id_chennal == Config.pamper_channels['Биржевик | VipPirates']:
            birgewik_reading(text, tiker)
        # if id_chennal == Config.pamper_channels['Черных мастер Россия']:
        #     chernihMaster_reading(text, tiker)
        if id_chennal == Config.pamper_channels['СИГНАЛЫ от CASHFLOW']:
            cashflow_publick_reading(text, tiker)


#обработка сообщений из канала fast&text only, разных памперов , пересыл без картинок и кажется быстрее
@client.on(events.NewMessage(chats=Config.fast_id))
async def vip_channels_handler(event):
    id_chennal = event.message.chat_id  # достаем idчата или какнал от которо пришло сообщение
    text = event.message.message  # достаем только текст сообщени
    # print(text)
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))  # находим тикер в тексте
    header_message = str(event.message.message).split('\n')[0]#из каждого сообщения вырезаем заголовок , где указано с какого канала персыл
    if tiker == '🤷‍♂':  # если в тексте нет тикера MOEX
        print(f'В данном тексте не обнаружены текеры MOEX')
    else:  # если есть тикер в тексте
        if 'Переслано из K-trade' in  header_message:
            print('🥵🥵🥵🥵🥵🥵🥵 - K-trade')
            k_trade_reading(text, tiker)
        if 'Переслано из GP INTRADAY' in  header_message:
            print('🥵🥵🥵🥵🥵🥵🥵 - Goodwin Production')
            goodwin_reading(text, tiker)
        if 'Олег торгует' in  header_message:
            oleg_reading(text, tiker)
            print('🥵🥵🥵🥵🥵🥵🥵 - Олег торгует')
        if 'Клуб ProfitKing' in  header_message:
            print('🥵🥵🥵🥵🥵🥵🥵 - Клуб ProfitKing')
            ProfitKing_reading(text, tiker)
        if 'ВИП канал' in  header_message:
            print('🥵🥵🥵🥵🥵🥵🥵 - Чехов ВИП канал')
            chehov_reading(text, tiker)
        if 'Мастер Россия' in  header_message:
            print('🥵🥵🥵🥵🥵🥵🥵 - Черных мастер россия ')
            chernihMaster_reading(text, tiker)



#обработчик сообщений только из канала id из списка channel_pyblic_id
@client.on(events.NewMessage(chats=Config.channel_pyblic_id))
async def vip_channels_handler(event):
    # dialogs = await get_dialodgs()
    # print(dialogs)
    # достаем idчата или какнал от которо пришло сообщение
    id_chennal = event.message.chat_id
    # print(id_chennal)
    # достаем сообщение полное с медиа
    message = event.message
    # print(message)
    # достаем только текст сообщени
    text = event.message.message
    # основная функция обработки сообщений , добавления клавиатур с кнопками
    # находится в модуле all_funcctions.py
    await reader_create_button(text, event, message, id_chennal, f'🐢 🛂Public - channel🛂', Config.channel_pyblic_dict_reverse)


#обработчик сообщений только из канала id из списка channel_vip_id
@client.on(events.NewMessage(chats=Config.channel_vip_id))
async def vip_channels_handler(event):
    # достаем idчата или какнал от которо пришло сообщение
    id_chennal = event.message.chat_id
    # достаем сообщение полное с медиа
    message = event.message
    print(message.message)
    # достаем только текст сообщени
    text = event.message.message
    if id_chennal == Config.channel_vip_dict['31. Antrading Official +| VipPirates']:
        print(text)
    #основная функция обработки сообщений , добавления клавиатур с кнопками
    #находится в модуле all_funcctions.py
    await reader_create_button(text, event, message, id_chennal,f'🔸VIP-channel', Config.channel_vip_dict_reverse)


#обработчик сообщений только из канала id из списка news_vip_id
@client.on(events.NewMessage(chats=Config.news_vip_id))
async def vip_channels_handler(event):
    # достаем idчата или какнал от которо пришло сообщение
    id_chennal = event.message.chat_id
    # print(id_chennal)
    # достаем сообщение полное с медиа
    message = event.message
    # print(message)
    # достаем только текст сообщени
    text = event.message.message
    #основная функция обработки сообщений , добавления клавиатур с кнопками
    #находится в модуле all_funcctions.py
    await reader_create_button(text, event, message, id_chennal,f'📮 VIP-news', Config.news_vip_dict_reverse)







# @client.on(events.NewMessage())
# async def new(event):
#     dialogs = await get_dialodgs()
#     print(dialogs)




if __name__ == '__main__':
    # Запуск клиента Telethon
    client.start()
    # Запуск бота aiogram
    executor.start_polling(dp)
    # client.loop.run_until_complete(main())
    # client.loop.run_until_complete(get_dialodgs())

