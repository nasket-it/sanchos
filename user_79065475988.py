

# from telethon import *
# from secrete import Token
# from all_functions import get_keyword_tiker_moex, cashflow_publick_reading
# from Config import Config
#
#
# client2 = TelegramClient('my_account.session2', Token.api_id2, Token.api_hash2)
#
#
# @client2.on(events.NewMessage(chats=Config.pamper_channels_id))
# async def pamper_channels_handler(event):
#     id_chennal = event.message.chat_id# достаем idчата или какнал от которо пришло сообщение
#     text = event.message.message # достаем только текст сообщени
#     tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))# находим тикер в тексте
#     if tiker == '🤷‍♂': #если в тексте нет тикера MOEX
#         print(f'В данном тексте не обнаружены текеры MOEX')
#     else:#если есть тикер в тексте
#
#         if id_chennal == Config.pamper_channels['СИГНАЛЫ от CASHFLOW']:
#             cashflow_publick_reading(text, tiker)
#         # if id_chennal == Config.pamper_channels['МОСКОВСКИЙ ИНВЕСТОР']:
#         #     mosinvestor_publick_reading(text, tiker)
