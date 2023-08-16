from secrete import Token
# from message_reading import oleg_reading
from datetime import datetime
from telethon import *
from all_functions import *
from aiogram import Bot, Dispatcher , types, executor
# from user_79065475988 import client2
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

async def get_dialodgs():
    dialogs = await client.get_dialogs()
    dialogs = [f'{i.name} : {i.id}' for i in dialogs ]
    print(dialogs)

client2 = TelegramClient('my_account.session2', Token.api_id2, Token.api_hash2)
client = TelegramClient('my_account.session', api_id, api_hash)


#обработка входящих сообщений телеграм на номер client2
@client2.on(events.NewMessage())
async def client2_channels_handler(event):
    id_chennal = event.message.chat_id # достаем idчата или какнал от которо пришло сообщение
    message = event.message # достаем сообщение полное с медиа
    text = event.message.message # достаем только текст сообщени
    user_id = event.message.from_id # достаём id юзера
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex)) # находим тикер в тексте
    if id_chennal in Config.channel_vip_vip_id:#обработчик сообщений только из канала id из списка channel_vip_vip_id
        time_now = str(datetime.now())[11:-4]
        await reader_create_button(text, event, message, id_chennal, f'📬VIP_VIP-channel\n -- {time_now} 🕰',
                                   Config.channel_vip_vip_reverse)
        if tiker == '🤷‍♂':  # если в тексте нет тикера MOEX
            print(f'В данном тексте не обнаружены текеры MOEX')
        else:  # если есть тикер в тексте
            if id_chennal == Config.channel_vip_vip['Мастер Россия💰']:
                time_now = str(datetime.now())[11:-4]
                print('🚀 - Мастер Россия💰', time_now)
                chernihMaster_reading(text, tiker)
            if id_chennal == Config.channel_vip_vip['Биржевик VIP | Инвестиции и Трейдинг💰']:
                time_now = str(datetime.now())[11:-4]
                print('🚀 - Биржевик VIP💰', time_now)
                birgewik_reading(text, tiker)
            if id_chennal == Config.channel_vip_vip['ВИП канал💰']:
                time_now = str(datetime.now())[11:-4]
                print('🚀 - Чехов ВИП канал💰', time_now)
                chehov_reading(text, tiker)


#обработка входящих сообщений телеграм на номер client
@client.on(events.NewMessage())
async def client_channels_handler(event):
    id_chennal = event.message.chat_id  # достаем idчата или какнал от которо пришло сообщение
    message = event.message  # достаем сообщение полное с медиа
    text = event.message.message  # достаем только текст сообщени
    # user_id = message.from_id.user_id # достаём id юзер
    # username = user_id.username
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))  # находим тикер в тексте
    if id_chennal in Config.pamper_channels_id:
        if tiker == '🤷‍♂':  # если в тексте нет тикера MOEX
            print(f'В данном тексте не обнаружены текеры MOEX')
        else:  # если есть тикер в тексте
            if id_chennal == Config.pamper_channels['СИГНАЛЫ от CASHFLOW']:
                cashflow_publick_reading(text, tiker)
            if id_chennal == Config.pamper_channels['МОСКОВСКИЙ ИНВЕСТОР']:
                mosinvestor_publick_reading(text, tiker)
    if id_chennal == Config.fast_id:
        header_message = str(event.message.message).split('\n')[0]  # из каждого сообщения вырезаем заголовок , где указано с какого канала персыл
        if tiker == '🤷‍♂':  # если в тексте нет тикера MOEX
            print(f'В данном тексте не обнаружены текеры MOEX')
        else:  # если есть тикер в тексте
            if 'Переслано из K-trade' in header_message:
                print('🥵💸 - K-trade')
                k_trade_reading(text, tiker)
            if 'Переслано из GP INTRADAY' in header_message:
                print('🥵💸 - Goodwin Production')
                goodwin_reading(text, tiker)
            # if 'Олег торгует' in  header_message:
            #     oleg_reading(text, tiker)
            #     print('🥵💸 - Олег торгует')
            if 'Клуб ProfitKing' in header_message:
                print('🥵💸 - Клуб ProfitKing')
                ProfitKing_reading(text, tiker)
            if 'ВИП канал' in header_message:
                print('🥵💸 - Чехов ВИП канал')
                chehov_reading(text, tiker)
            if 'РФ+США' in header_message:
                print('🥵💸 - Черных мастер россия ')
                chernihMaster_reading(text, tiker)
            if 'Premium СИГНАЛЫ' in header_message:
                print('🥵💸 - Premium СИГНАЛЫ  ')
                cashflow_vip_reading(text, tiker)
    if id_chennal in Config.channel_pyblic_id:
        time_now = str(datetime.now())[11:-4]
        await reader_create_button(text, event, message, id_chennal, f'🐢 🛂Public - channel\n -- {time_now} 🕰',Config.channel_pyblic_dict_reverse)
    if id_chennal in Config.channel_vip_id:
        time_now = str(datetime.now())[11:-4]
        await reader_create_button(text, event, message, id_chennal, f'🔸VIP-channel\n -- {time_now} 🕰',Config.channel_vip_dict_reverse)
        if id_chennal == Config.channel_vip_dict['Коган | VipPirates']:
            print('🥵💸 Коган | VipPirates')
            kogan_vip_reading(text, tiker)
    if id_chennal in Config.news_vip_id:
        time_now = str(datetime.now())[11:-4]
        await reader_create_button(text, event, message, id_chennal, f'📮 VIP-news\n -- {time_now} 🕰',Config.news_vip_dict_reverse)
    if id_chennal == Config.tdmap_channels_id:
        if message.from_id.user_id == Config.tdmap_user_id:
            print(f'💂💂 - написал TDmap')
            try:
                await reader_create_button(text, event, message, id_chennal, f'💂‍💂💂‍ - TDmap - 🪧',Config.tdmap_channels_reverse)
            except:
                print('user_id - не обнаружено')











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





if __name__ == '__main__':
    # Запуск клиента Telethon
    client.start()
    client2.start()
    # Запуск бота aiogram
    executor.start_polling(dp)
    # client.loop.run_until_complete(main())
    # client.loop.run_until_complete(get_dialodgs())

