
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

def add_expense(raw_message: str) -> Expense:
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)
    inserted_row_id = db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Expense(amount = parsed_message.amount, category_name= category.name)

def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise Exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_today_statistics() -> str:
    """Возвращает строкой статистику расходов за сегодня"""
    cursor = db.get_cursor()
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

def get_month_statistics() -> str:
    """Возвращает строкой статистику расходов за текущий месяц"""
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) from expense where date(created) >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце ещё нет расходов"
    all_today_expenses = result[0]
    cursor.execute(f"select sum(amount) "
                   f"from expense where date(created) >= '{first_day_of_month}' "
                   f"and category_codename in (select codename "
                   f"from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0

    return (f"Расходы в текущем месяце:\n"
            f"всего — {all_today_expenses} руб.\n"
            f"базовые — {base_today_expenses} руб. из "
            f"{30 * _get_budget_limit()} руб.\n")


def get_all_statistics_per_month() -> str:
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"SELECT  amount, "
        f"(SELECT category.name FROM category "
        f"WHERE category.codename = expense.category_codename) AS CName "
        f"FROM expense where date(created) >= '{first_day_of_month}'")
        # f"where created > current_date - interval '1 week'; >= '{first_day_of_month}'")
    result = cursor.fetchall()


    if not result[0]:
        return "В этом месяце ещё нет расходов"
    dt = {}
    for i in range(len(result)):
        if result[i][1] not in dt:
            dt[result[i][1]] = result[i][0]
        else:
            dt[result[i][1]] += result[i][0]
    dt

    # all_stats = dict((y, x) for x, y in result)
    return (f"Всего потрачено \n"
            f"{[(k, v) for k, v in dt.items()]}")

def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _get_budget_limit() -> int:
    """Возвращает дневной лимит трат для основных базовых трат"""
    return db.fetchall("budget", ["daily_limit"])[0]["daily_limit"]

def get_all_AllExpenses() -> str:
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"SELECT  amount, "
                   f"(SELECT category.name FROM category "
                   f"WHERE category.codename = expense.category_codename) AS CName "
                   f"FROM expense ")
    # f"where created > current_date - interval '1 week'; >= '{first_day_of_month}'")
    result = cursor.fetchall()
    if not result[0]:
        return "В этом месяце ещё нет расходов"
    dt = {}
    for i in range(len(result)):
        if result[i][1] not in dt:
            dt[result[i][1]] = result[i][0]
        else:
            dt[result[i][1]] += result[i][0]
    dt

    # all_stats = dict((y, x) for x, y in result)
    return dt
