import psycopg2
from typing import Dict, List, Tuple
from typing import List, NamedTuple, Optional
import db


class Message(NamedTuple):
    amount: int
    category_text: str

class Expense(NamedTuple):
    amount: int
    category_name: str


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
