import psycopg2
from psycopg2 import Error
from psycopg2 import OperationalError
from typing import Dict, List, Tuple
import datetime
import pytz
from typing import List, NamedTuple, Optional
import db
import Exceptions
from categories import Categories
import datetime
import re
import pytz

class Message(NamedTuple):
    amount: int
    category_text: str

class Expense(NamedTuple):
    amount: int
    category_name: str

# # def create_connection(db_name, db_user, db_password, db_host, db_port):
# #     connection = None
# #     try:
# #         connection = psycopg2.connect(
# #             database=db_name,
# #             user=db_user,
# #             password=db_password,
# #             host=db_host,
# #             port=db_port,
# #         )
# #         print("Connection to PostgreSQL DB successful")
# #     except OperationalError as e:
# #         print(f"The error '{e}' occurred")
# #     return connection
#
#     # Подключение к существующей базе данных
# def _get_now_formatted() -> str:
#     """Возвращает сегодняшнюю дату строкой"""
#     tz = pytz.timezone("Europe/Moscow")
#     now = datetime.datetime.now(tz)
#     return now.strftime("%Y-%m-%d %H:%M:%S")
#
#
# def insert(table: str, column_values: Dict):
#     conn=psycopg2.connect("dbname='telegbotdb1' user='postgres' password='123' host='localhost' port='5432'")
#     cursor = conn.cursor()
#     columns = ', '.join(column_values.keys())
#     values = list(column_values.values())
#     placeholders = ', '.join( ['%s'] * len(column_values))
#     sql = " INSERT INTO %s ( %s ) VALUES ( %s ) " % (table, columns, placeholders)
#     cursor.execute(sql, values)
#     conn.commit()
#
#
# def fetchall(table: str, columns: List[str]) -> List[Tuple]:
#     conn = psycopg2.connect("dbname='telegbotdb1' user='postgres' password='123' host='localhost' port='5432'")
#     cursor = conn.cursor()
#     columns_joined = ", ".join(columns)
#     sql = "SELECT %s FROM %s " % (columns_joined, table)
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#     result = []
#     for row in rows:
#         dict_row = {}
#         for index, column in enumerate(columns):
#             dict_row[column] = row[index]
#         result.append(dict_row)
#     return result

#fetchall("expense", ["category_codename", "raw_text"])

#insert("expense", {"amount":100, "created":datetime.date(2012, 12, 14), "category_codename":"dinner", "raw_text":"обед в ресторане"})





# def insert(item, quantity, price):
#     conn=psycopg2.connect("dbname='telegbotdb1' user='postgres' password='123' host='localhost' port='5432'")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO store VALUES('%s','%s','%s')" % (item, quantity, price))
#     conn.commit()
#     conn.close()


#create_table()
# insert('coffee cup', 7, 100)

def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    conn = psycopg2.connect("dbname='telegbotdb1' user='postgres' password='123' host='localhost' port='5432'")
    cursor = conn.cursor()
    columns_joined = ", ".join(columns)
    sql = "SELECT %s FROM %s " % (columns_joined, table)
    cursor.execute(sql)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result

def get_today_statistics() -> str:
    """Возвращает строкой статистику расходов за сегодня"""
    conn = psycopg2.connect("dbname='telegbotdb1' user='postgres' password='123' host='localhost' port='5432'")
    cursor = conn.cursor()
    cursor.execute("select sum(amount) from expense where date(created)=current_date")
    result = cursor.fetchone()

    if not result[0]:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result[0]
    cursor.execute("select sum(amount) from expense where date(created)=current_date " 
                    "and "
                    "category_codename in (select codename from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    # return base_today_expenses
    return (f"Расходы сегодня:\n"
            f"всего — {all_today_expenses} руб.\n"
            f"базовые — {base_today_expenses} руб. из {_get_budget_limit()} руб.\n\n"
            f"За текущий месяц: /month")
#
def _get_budget_limit() -> int:
    """Возвращает дневной лимит трат для основных базовых трат"""
    return db.fetchall("budget", ["daily_limit"])[0]["daily_limit"]

print(get_today_statistics())
