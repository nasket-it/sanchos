
import asyncio
import sqlite3
from function_sqlite3 import prosmotr_sqlite
from functions_pamperov import start_stop_db




def update_value_db(value, name_chenal, column = 'start_stop', name_table = 'statr_stop_zakupki'):
    #value - знасчение на которое нцжну обновить
    #tiker - id , первый столбец в котором тикеры
    #column - назнание столбаца в котором будут изменения
    #mame_table - название таблицы , по умолчанию 'statr_stop_zakupki'
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    # Обновление значения в таблице
    record_id = 1  # Идентификатор записи, которую нужно обновить
    cursor.execute(f'''UPDATE {name_table} SET {column} = ? WHERE name_chenal = ?''', (value, name_chenal))

    conn.commit()
    conn.close()


async def proverka_comand(text, bot ):
    if str(text).lower()[-4:]  == 'stop' and str(text).lower()[:-5] in list_chenal:
        update_value_db(0, str(text).lower()[:-5])
        message_status = f'❌{str(text).lower()[:-5]} - закупка отключена'
        await bot.send_message(-1001701470058, f'{message_status}')
    if  str(text).lower()[-5:]  == 'start' and str(text).lower()[:-6] in list_chenal:
        update_value_db(1, str(text).lower()[:-6])
        message_status = f'✅{str(text).lower()[:-6]} - закупка включена'
        await bot.send_message(-1001701470058, f'{message_status}')


async def status_start_stop_chenal():
    status = f''
    for i in prosmotr_sqlite('*', 'statr_stop_zakupki'):
        if i[1] == 0 and i[0] != 'flag_start_stop_allpokupki':
            status += f"🧢  {i[0]} - ❌\n"
        if i[1] == 1 and i[0] != 'flag_start_stop_allpokupki':
            status += f"🧢  {i[0]} - ✅\n"
        if i[1] == 0 and i[0] == 'flag_start_stop_allpokupki':
            status += f"🪖  {i[0]} - ❌\n"
        if i[1] == 1 and i[0] == 'flag_start_stop_allpokupki':
            status += f"🪖  {i[0]} - ✅\n"
    return status




flag_start_stop_pokupki = True
list_chenal = ['masinvestor', 'fibo_vip', 'cashflou_public', 'unique_public',
               'goodwin_vip', 'venividivici_vip', 'oleg_public', 'k_trade',
               'chehov_vip', 'birgevik_vip', 'profit_king_vip', 'chernihmaster_vip',
               'cashflow_vip', 'kogan_vip']



async def comand_telegram(event, bot):
    global flag_start_stop_pokupki
    id_chennal = event.message.chat_id  # достаем idчата или какнал от которо пришло сообщение
    message = event.message  # достаем сообщение полное с медиа
    text = event.message.message  # достаем только текст сообщени
    if len(text) == 5 and str(text).upper() == 'START':
        update_value_db(1, 'flag_start_stop_allpokupki')
        if bool(*start_stop_db('flag_start_stop_allpokupki')) == True:
            await bot.send_message(-1001701470058, '💸❗️ Общая закупка разрешена - ✅')
    if  len(text) == 4 and str(text).upper() == 'STOP':
        update_value_db(0, 'flag_start_stop_allpokupki')
        if bool(*start_stop_db('flag_start_stop_allpokupki')) == False:
            await bot.send_message(-1001701470058, '❗Общая закупка запрещена - ❌')
    if  len(text) == 4 and str(text).upper() == 'FLAG':
        if bool(*start_stop_db('flag_start_stop_allpokupki')) == True:
            message_status = '💸❗️ Общая закупка разрешена - ✅\n📗 Публикация новостей - ✅\n🤑 Публикация сигналов - ✅'
            await bot.send_message(-1001701470058, f'{message_status}')
        if bool(*start_stop_db('flag_start_stop_allpokupki')) == False:
            message_status = '💸️❗ Общая закупка запрещена - ❌\n📗 Публикация новостей - ✅\n🤑 Публикация сигналов - ✅'
            await bot.send_message(-1001701470058, f'{message_status}')


    #команды для управления закупками на отдельные каналы
    if str(text).lower() == 'status':
        status_all_chenal = await status_start_stop_chenal()
        await bot.send_message(-1001701470058, f'{status_all_chenal}')


    await proverka_comand(text,bot)




