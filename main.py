import subprocess
from telethon import *
from all_functions import *
from aiogram import Bot, Dispatcher , types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from AlorPy import AlorPy  # Работа с Alor OpenAPI V2
from Config import Config  # Файл конфигурации
from secrete import Token



API_TOKEN = Token.bot_token


# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


exchange = 'MOEX'  # Код биржи MOEX или SPBX
symbol = 'SBER'  # Тикер
port_io = Token.alor_portfolio





account = ['-1001892817733','-1001857334624']




client = TelegramClient('my_account.session', Token.api_id,Token.api_hash)



#в этой переменной храниться последнее сообщение отправленное в канал новостоной
#перед отправкой следующего сообщения проверяется текст этого , для предотращения дублей
check1 = 0
all_signals = []



#получаем все диалоги , функция корутина (запускается в самом низу листа )
# async def main():
#     dialogs = await client.get_dialogs()
#     dialogs = [f'{i.name} : {i.id}' for i in dialogs]
#     print(dialogs)




@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # await bot.send_message(message.chat.id, 'Привет')
    subprocess.Popen(["python", "/path/to/your/script.py"])
    await message.reply("Скрипт запущен.")




#щбработчик нажатия инлайн кнопок
@dp.callback_query_handler()
async def buttons_press(callback_query):
    print(callback_query.data)
    if str(callback_query.data).split()[0] == '2':
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




# обработчик сообщений из каналов памперов , обрабатывает и автоматически покупает
@client.on(events.NewMessage(chats=Config.pamper_channels_id))
async def pamper_channels_handler(event):
    id_chennal = event.message.chat_id# достаем idчата или какнал от которо пришло сообщение
    text = event.message.message # достаем только текст сообщени
    tiker = str(get_keyword_tiker_moex(text, Config.tickers_moex))# находим тикер в тексте
    if tiker == '🤷‍♂': #если в тексте нет тикера MOEX
        print(f'В данном тексте не обнаружены текеры MOEX')
    else:#если есть тикер в тексте
        # если сообщение от канала РДВ Premium | SS PRO
        if id_chennal == Config.pamper_channels['РДВ Premium | SS PRO']:
            keyword_RDV = ['OТКPЫТИE', 'LONG', 'CPOК', 'ИДEИ:', 'ДO'] #ключевые слова на покупку сигнала из сообщений этого канала
            if keyword_search(text, keyword_RDV):# если в тексте сообщения есть ВСЕ!!! слова ключевые
                buy = 'buy'# покупаем или продаем , настраивается вручную
                summ = '100000'# сумма покупки , насраивается вручную
                create_limit_order(tiker, buy, summ, 0)# функция покупки
        # если сообщение от канала K-Trade | SS Exclusive'
        if id_chennal == Config.pamper_channels['K - trade']:
            keyword_KTrade = ['ЛОНГ', 'ВХОД:']
            keyword_KTrade1 = ['ЗАХОДИМ', 'СПЕКУЛЯТИВНО']
            keyword_KTrade2 = ['МОЖНО', 'ЗАЙТИ']
            keyword_KTrade3 = ['МОЖНО', 'ВЗЯТЬ']
            if keyword_search(text, keyword_KTrade) or keyword_search(text,keyword_KTrade1) or keyword_search(text,keyword_KTrade2) or keyword_search(text,keyword_KTrade3) :
                buy = 'buy'
                summ = '150000'
                print('long')
                create_limit_order(tiker, buy, summ, 0)
        # если сообщение от канала Олег торгует
        if id_chennal == Config.pamper_channels['Олег торгует']:
            keyword_Oleg1 = ['#ИДЕЯ', 'ЛОНГ','ВХОД']
            keyword_Oleg2 = ['ИДЕЯ', 'ЛОНГ','ВХОД']
            if keyword_search(text, keyword_Oleg1) or keyword_search(text,keyword_Oleg2) :
                buy = 'buy'
                summ = '70000'
                print('long')
                create_limit_order(tiker, buy, summ, 0)
        # если сообщение от канала Goodwin Production |GP Fund | 💎 | SS PRO Exclusive
        if id_chennal == Config.pamper_channels['Goodwin Production |GP Fund | 💎 | SS PRO Exclusive']:
            keyword_Goodwin1 = ['ПОКУПКА', 'СТОП','ПРОФИТЫ']
            keyword_Goodwin2 = ['ПОКУПКА', 'СТОП','ПРОФИТ']
            if keyword_search(text, keyword_Goodwin1) or keyword_search(text,keyword_Goodwin2):
                buy = 'buy'
                summ = '150000'
                print('long')
                create_limit_order(tiker, buy, summ, 0)

        if id_chennal == Config.pamper_channels['Чехов ВИП канал']:
            keyword1 = ['ПРИКУПИТЕ', 'НЕМНОГО']
            keyword2 = ['ПРИКУПИМ', 'НЕМНОГО']
            keyword3 = ['ПОКУПАЕМ', 'НЕМНОГО']
            keyword4 = ['ПОКУПАЮ', 'НЕМНОГО']
            if keyword_search(text, keyword1) or keyword_search(text,keyword2) or keyword_search(text,keyword3) or keyword_search(text,keyword4):
                buy = 'buy'
                summ = '200000'
                print('long')
                create_limit_order(tiker, buy, summ, 0)

        if id_chennal == Config.pamper_channels['Клуб ProfitKing']:
                    keyword1 = ['КУПИЛ']
                    keyword2 = ['ПОКУПКА']
                    keyword3 = ['ВЗЯЛ']
                    keyword4 = ['ПОКУПАЮ']
                    if len(str(text).split()) <= 8 and  keyword_search(text,keyword2) or keyword_search(text,keyword3) or keyword_search(text,keyword4) or keyword_search(text,keyword1):
                        buy = 'buy'
                        summ = '200000'
                        print('long')
                        create_limit_order(tiker, buy, summ, 0)





#обработчик сообщений только из канала id из списка channel_pyblic_id
@client.on(events.NewMessage(chats=Config.channel_pyblic_id))
async def vip_channels_handler(event):
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





if __name__ == '__main__':
    # Запуск клиента Telethon
    client.start()
    # Запуск бота aiogram
    executor.start_polling(dp)
    # client.loop.run_until_complete(main())
    # client.loop.run_until_complete(get_dialodgs())

