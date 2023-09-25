import sqlite3
from Config import Config


import sqlite3

data = ('NKL',0.32, 0.57, 4.55, 0.98, 6.45, 3.44, 3.45, 0.767, 6.76, 34.09)

# def insert_data_sql():
#     with sqlite3.connect('my_database.db') as conn:
#         # Создание объекта курсора, который будет выполнять SQL-запросы
#         cursor = conn.cursor()
#         cursor.execute("""INSERT INTO stakani VALUES()"""
#         conn.commit()


def delete_zapis(name):
    with sqlite3.connect('my_database.db') as conn:
        # Создание объекта курсора, который будет выполнять SQL-запросы
        cursor = conn.cursor()
        cursor.execute(f""" DELETE * FROM {name}  """)
        conn.commit()


# Создание таблицы
def create_table_sqlite():
    # Создание подключения к базе данных. Если базы данных не существует, то она будет создана
   with sqlite3.connect('my_database.db') as conn:
        # Создание объекта курсора, который будет выполнять SQL-запросы
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS statr_stop_zakupki (id INTEGER PRIMARY KEY, is_active INTEGER)''')
        conn.commit()

def prosmotr_sqlite(column, name_table, name_chenal = None ):
    with sqlite3.connect('my_database.db') as conn:
        # Создание объекта курсора, который будет выполнять SQL-запросы
        cursor = conn.cursor()
        if name_chenal != None:
            # Выполнение запроса SELECT для получения всех записей из таблицы
            cursor.execute(f"SELECT {column} FROM {name_table} WHERE name_chenal = '{name_chenal}'")
            # Получение всех записей из таблицы
            row = cursor.fetchall()
            return row[0]
        else:
            cursor.execute(f"SELECT {column} FROM {name_table}")
            # Получение всех записей из таблицы
            row = cursor.fetchall()
            return row
        # Вывод записей
        # for row in row:
        #     print(row)
def add_value(name_chenal, start_stop):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Добавление значения в таблицу
    cursor.execute('''INSERT INTO statr_stop_zakupki (name_chenal, start_stop) VALUES (?, ?)''', (name_chenal, start_stop))

    conn.commit()
    conn.close()


mosinvestor_flag = True
fibo_flag = True
cashflou_public_flag = True
unique_flag = True
goodwin_flag = True
venividivici_vip_flag = True
oleg_flag = True


# create_table_sqlite()
# add_value('kogan_vip', 0)
print(prosmotr_sqlite('*', 'statr_stop_zakupki'))

#     if i[1] == 0:
#         print(f"{i[0]} - 🔴Закупка выключена" )
#     print(i)


class Symbol:
    def __init__(self, symbol):
        self.symbol = symbol
        self.symbol = self.prosmotr_sqlite("symbol", self.symbol)
        self.shortname = self.prosmotr_sqlite("shortname", self.symbol)
        self.description = self.prosmotr_sqlite("description", self.symbol)
        self.exchange = self.prosmotr_sqlite("exchange", self.symbol)
        self.type = self.prosmotr_sqlite("type", self.symbol)
        self.lotsize = self.prosmotr_sqlite("lotsize", self.symbol)
        self.facevalue = self.prosmotr_sqlite("facevalue", self.symbol)
        self.cfiCode = self.prosmotr_sqlite("cfiCode", self.symbol)
        self.cancellation = self.prosmotr_sqlite("cancellation", self.symbol)
        self.minstep = self.prosmotr_sqlite("minstep", self.symbol)
        self.rating = self.prosmotr_sqlite("rating", self.symbol)
        self.marginbuy = self.prosmotr_sqlite("marginbuy", self.symbol)
        self.marginsell = self.prosmotr_sqlite("marginsell", self.symbol)
        self.marginrate = self.prosmotr_sqlite("marginrate", self.symbol)
        self.pricestep = self.prosmotr_sqlite("pricestep", self.symbol)
        self.priceMax = self.prosmotr_sqlite("priceMax", self.symbol)
        self.priceMin = self.prosmotr_sqlite("priceMin", self.symbol)
        self.theorPrice = self.prosmotr_sqlite("theorPrice", self.symbol)
        self.theorPriceLimit = self.prosmotr_sqlite("theorPriceLimit", self.symbol)
        self.volatility = self.prosmotr_sqlite("volatility", self.symbol)
        self.currency = self.prosmotr_sqlite("currency", self.symbol)
        self.ISIN = self.prosmotr_sqlite("ISIN", self.symbol)
        # self.yield = self.prosmotr_sqlite("yield", self.symbol)
        self.board = self.prosmotr_sqlite("board", self.symbol)
        self.primary_board = self.prosmotr_sqlite("primary_board", self.symbol)
        self.tradingStatus = self.prosmotr_sqlite("tradingStatus", self.symbol)
        self.tradingStatusInfo = self.prosmotr_sqlite("tradingStatusInfo", self.symbol)
        self.complexProductCategory = self.prosmotr_sqlite("complexProductCategory", self.symbol)
        self.priceMultiplier = self.prosmotr_sqlite("priceMultiplier", self.symbol)
        self.priceShownUnits = self.prosmotr_sqlite("priceShownUnits", self.symbol)

    def prosmotr_sqlite(self, column, symbol):
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT {column} FROM stocks WHERE symbol = '{symbol}'")
        row = cursor.fetchone()
        conn.close()

        if row is not None:
            return row[0]
        else:
            return None


ABRD = Symbol("ABRD")
print(ABRD.minstep)

# for i in Config.info['ETLN']:
#     print(f'self.{i} = self.prosmotr_sqlite("{i}", self.symbol)')


# for symbol, values in Config.info.items():
#     cursor.execute('''
#         INSERT INTO stocks VALUES
#         (:symbol, :shortname, :description, :exchange, :type, :lotsize, :facevalue, :cfiCode,
#         :cancellation, :minstep, :rating, :marginbuy, :marginsell, :marginrate, :pricestep,
#         :priceMax, :priceMin, :theorPrice, :theorPriceLimit, :volatility, :currency, :ISIN,
#         :yield, :board, :primary_board, :tradingStatus, :tradingStatusInfo,
#         :complexProductCategory, :priceMultiplier, :priceShownUnits)
#     ''', values)

# Зафиксировать изменения и закрыть соединение с базой данных
# conn.commit()
# conn.close()