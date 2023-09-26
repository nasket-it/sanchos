from secrete import Token
# from message_reading import oleg_reading
from datetime import datetime
from photo_text import photo_to_text, download_photo, filter_words_rus_en
from telethon import *
from all_functions import *
from aiogram import Bot, Dispatcher , types, executor
# from user_79065475988 import client2
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from functions_pamperov import *
from keywords import Keywords, Risck
from Config import Config  # Файл конфигурации
from bs4 import BeautifulSoup
from audio_text import esli_voice_to_text_ili_text_text
from tiinvest_stream import data_dict, main1
import uuid
import os
import asyncio
from upravlenie_program_comand import comand_telegram, flag_start_stop_pokupki



# flag_start_stop_pokupki = True




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
    dialogs = await client2.get_dialogs()
    dialogs = [f'{i.name} : {i.id}' for i in dialogs ]
    print(dialogs)

client2 = TelegramClient('my_account.session2', Token.api_id2, Token.api_hash2)
client = TelegramClient('my_account.session', api_id, api_hash)


def main():
    asyncio.run(main1())
    print([i for i in data_dict])
#обработка входящих сообщений телеграм на номер client2
@client2.on(events.NewMessage(chats=Config.channel_vip_vip_id))
async def client2_channels_handler(event):
    # await delete_oga_files()
    # await get_dialodgs()
    id_chennal = event.message.chat_id # достаем idчата или какнал от которо пришло сообщение
    message = event.message # достаем сообщение полное с медиа
    text = await esli_voice_to_text_ili_text_text(event)
    user_id = event.message.from_id # достаём id юзера
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex)) # находим тикер в тексте
    if id_chennal in Config.channel_vip_vip_id :#обработчик сообщений только из канала id из списка channel_vip_vip_id
        text = await esli_voice_to_text_ili_text_text(event)
        time_now = str(datetime.now())[11:-4]
        await reader_create_button(text, event, message, id_chennal, f'📬VIP_VIP-channel\n -- {time_now} 🕰',
                                   Config.channel_vip_vip_reverse,bot )
        if tiker == '🤷‍♂':  # если в тексте нет тикера MOEX
            print(f'В данном тексте не обнаружены текеры MOEX')
        else:  # если есть тикер в тексте
            if id_chennal == Config.channel_vip_vip['36.Goodwin | VipPirates']:
                time_now = str(datetime.now())[11:-4]
                if event.photo:
                    images = await download_photo(event, client2)
                    text = photo_to_text(images)
                    text = filter_words_rus_en(str(text).split())
                    await reader_create_button(text, event, message, id_chennal, f'📬VIP_VIP-channel\n -- {time_now} 🕰',
                                               Config.channel_vip_vip_reverse, bot)
            if id_chennal == Config.channel_vip_vip['38. VENIVIDIVICI PRESTIGE | VipPirates'] and bool(*start_stop_db('flag_start_stop_allpokupki')) :
                time_now = str(datetime.now())[11:-4]
                print('🥵💸 38. VENIVIDIVICI PRESTIGE | VipPirates')
                await client2.send_message(-1001701470058, f'🔘🔘 Тест \n 🕠 {time_now} \n {text}')
                await venividivici_vip_reading(text, tiker, bot)
            if id_chennal == Config.channel_vip_vip['ВИП канал💰'] and bool(*start_stop_db('flag_start_stop_allpokupki')):
                if event.message.voice:
                    print('voice')
                else:
                    time_now = str(datetime.now())[11:-4]
                    print('🚀 - Чехов ВИП канал💰', time_now)
                    await chehov_reading(text, tiker, bot)
            if id_chennal == Config.channel_vip_vip['45 K-Trade| VipPirates'] and bool(*start_stop_db('flag_start_stop_allpokupki')):
                time_now = str(datetime.now())[11:-4]
                print('🚀 - 45 K-Trade| VipPirates', time_now)
                await k_trade_reading(text, tiker, bot)


#обработка входящих сообщений телеграм на номер client
@client.on(events.NewMessage())
async def client_channels_handler(event):
    await delete_oga_files()
    # await main1()
    # print(len(data_dict))
    global text1
    id_chennal = event.message.chat_id  # достаем idчата или какнал от которо пришло сообщение
    message = event.message  # достаем сообщение полное с медиа

    text = event.message.message # достаем только текст сообщени
    # if event.chat.title:
    #     title = event.chat.title #название канала
    #     print(text , id_chennal, title)
    # user_id = message.from_id.user_id # достаём id юзер
    # username = user_id.username
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))  # находим тикер в тексте
    if id_chennal in Config.pamper_channels_id:
        if tiker == '🤷‍♂':  # если в тексте нет тикера MOEX
            print(f'В данном тексте не обнаружены текеры MOEX')
        else:  # если есть тикер в тексте
            if id_chennal == Config.pamper_channels['СИГНАЛЫ от CASHFLOW'] and bool(*start_stop_db('flag_start_stop_allpokupki')) :
                await cashflow_publick_reading(text, tiker, bot)
            if id_chennal == Config.pamper_channels['МОСКОВСКИЙ ИНВЕСТОР'] and bool(*start_stop_db('flag_start_stop_allpokupki')) :
                await mosinvestor_publick_reading(text, tiker, bot)
            if id_chennal == Config.pamper_channels['UNIQUE TRADE 🐥'] and bool(*start_stop_db('flag_start_stop_allpokupki')) :
                await unique_trade(text, tiker, bot)
            if id_chennal == Config.pamper_channels['Fibo Trade VIP (ValSi пересыл)'] and bool(*start_stop_db('flag_start_stop_allpokupki')):
                await fibo_vip(text, tiker, bot)
    if id_chennal == Config.fast_id:
        header_message = str(event.message.message).split('\n')[0]  # из каждого сообщения вырезаем заголовок , где указано с какого канала персыл
        if tiker == '🤷‍♂':  # если в тексте нет тикера MOEX
            print(f'В данном тексте не обнаружены текеры MOEX')
        else:  # если есть тикер в тексте
            if 'Переслано из K-trade' in header_message and bool(*start_stop_db('flag_start_stop_allpokupki')):
                print('🥵💸 - K-trade')
                await k_trade_reading(text, tiker, bot)
            if 'Переслано из GP INTRADAY' in header_message and bool(*start_stop_db('flag_start_stop_allpokupki')):
                print('🥵💸 - Goodwin Production')
                await goodwin_reading(text, tiker, bot)
            if 'Олег торгует' in  header_message and bool(*start_stop_db('flag_start_stop_allpokupki')):
                await oleg_reading(text, tiker, bot)
                print('🥵💸 - Олег торгует')
            if 'Клуб ProfitKing' in header_message and bool(*start_stop_db('flag_start_stop_allpokupki')):
                print('🥵💸 - Клуб ProfitKing')
                await ProfitKing_reading(text, tiker, bot)
            if 'ВИП канал' in header_message and bool(*start_stop_db('flag_start_stop_allpokupki')):
                print('🥵💸 - Чехов ВИП канал')
                await chehov_reading(text, tiker, bot)
            if 'РФ+США' in header_message and bool(*start_stop_db('flag_start_stop_allpokupki')):
                print('🥵💸 - Черных мастер россия ')
                await chernihMaster_reading(text, tiker, bot)
            if 'Premium СИГНАЛЫ' in header_message and bool(*start_stop_db('flag_start_stop_allpokupki')):
                print('🥵💸 - Premium СИГНАЛЫ  ')
                await cashflow_vip_reading(text, tiker, bot)
    if id_chennal in [-1001574832908, -1001848353901, -1001854614186]:
        text1 = await esli_voice_to_text_ili_text_text(event)
        if tiker != '🤷‍♂' and bool(*start_stop_db('flag_start_stop_allpokupki')):
            await chernihMaster_reading(text1, tiker, bot)
        await reader_create_button(text1, event, message, id_chennal, f'🕰',Config.channel_vip_dict_reverse, bot)

    if id_chennal == -1001854614186:
        pass

    if id_chennal in Config.channel_pyblic_id:
        time_now = str(datetime.now())[11:-4]
        await reader_create_button(text, event, message, id_chennal, f'🐢 🛂Public - channel\n -- {time_now} 🕰',Config.channel_pyblic_dict_reverse, bot)
    if id_chennal in Config.channel_vip_id:
        time_now = str(datetime.now())[11:-4]
        await reader_create_button(text, event, message, id_chennal, f'🔸VIP-channel\n -- {time_now} 🕰',Config.channel_vip_dict_reverse, bot)
        if id_chennal == Config.channel_vip_dict['Коган | VipPirates'] and bool(*start_stop_db('flag_start_stop_allpokupki')):
            print('🥵💸 Коган | VipPirates')
            await kogan_vip_reading(text, tiker, bot)
        if id_chennal == Config.channel_vip_dict['38. VENIVIDIVICI PRESTIGE | VipPirates'] and bool(*start_stop_db('flag_start_stop_allpokupki')):
            print('🥵💸 VENIVIDIVICI PRESTIGE | VipPirates')
            await venividivici_vip_reading(text, tiker, bot)
    if id_chennal in Config.news_vip_id:
        time_now = str(datetime.now())[11:-4]
        await reader_create_button(text, event, message, id_chennal, f'📮 VIP-news\n -- {time_now} 🕰',Config.news_vip_dict_reverse, bot)
    if id_chennal == Config.tdmap_channels_id:
        if message.from_id.user_id == Config.tdmap_user_id:
            print(f'💂💂 - написал TDmap')
            try:
                await reader_create_button(text, event, message, id_chennal, f'💂‍💂💂‍ - TDmap - 🪧',Config.tdmap_channels_reverse, bot)
            except:
                print('user_id - не обнаружено')



name_channal = {'name' : ''}
start = ''
#обработчик только свои исходящих сообщений и только в определенный канал , также отключает или включает закупку акций
#программой , можно посмотреть статус программы , работает закупка или нет
@client.on(events.NewMessage(chats=-1001701470058, incoming=False))
async def client_channels_handler(event):
    await comand_telegram(event, bot)
    # global flag_start_stop_pokupki
    # id_chennal = event.message.chat_id  # достаем idчата или какнал от которо пришло сообщение
    # message = event.message  # достаем сообщение полное с медиа
    # text = event.message.message  # достаем только текст сообщени
    # if len(text) == 5 and str(text).upper() == 'START':
    #     flag_start_stop_pokupki = True
    #     await client.send_message(-1001701470058, '🟢Закупка включена')
    # elif len(text) == 4 and str(text).upper() == 'STOP':
    #     flag_start_stop_pokupki = False
    #     await client.send_message(-1001701470058, '🔴Закупка выключена')
    # elif len(text) == 4 and str(text).upper() == 'FLAG':
    #     message_status = '🟢Закупка включена' if flag_start_stop_pokupki else '🔴Закупка выключена'
    #     await client.send_message(-1001701470058, f'{message_status}')
    #     print(flag_start_stop_pokupki)

#
#
#



#






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

# delete_oga_files()


if __name__ == '__main__':
    # main()
    # Запуск клиента Telethon
    client.start()
    client2.start()
    # Запуск бота aiogram
    executor.start_polling(dp)
    # client.loop.run_until_complete(main())
    # client.loop.run_until_complete(get_dialodgs())
    # asyncio.run(delete_oga_files())
    # asyncio.run(main1())



