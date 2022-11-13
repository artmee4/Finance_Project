from typing import Dict, List, NamedTuple

import db
import re
import Exceptions
from googletrans import Translator, constants

class Category(NamedTuple):
    """Структура категории"""
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]

class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий расходов из БД"""
        categories = db.fetchall(
            "category", "codename name is_base_expense aliases".split()
        )
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        """Заполняет по каждой категории aliases, то есть возможные
        названия этой категории, которые можем писать в тексте сообщения.
        Например, категория «кафе» может быть написана как cafe,
        ресторан и тд."""
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_base_expense=category['is_base_expense'],
                aliases=aliases
            ))
        return categories_result

    def get_all_categories(self) -> List[Dict]:
        """Возвращает справочник категорий."""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded


#TODO: добавить команды ниже для вызова из телеги
#Введите текст в следующем формате: название категории
# (прим: Здоровье, относится к базовым потребностям или нет (да/нет), алиасы (прим для здоровья: врач, лекарства, диетолог)
def add_category(raw_message: str):
    messageToInsert = parsed_message(raw_message)
    db.insert("category", {
        "codename": messageToInsert[0],
        "name": messageToInsert[1],
        "is_base_expense": messageToInsert[2],
        "aliases": messageToInsert[3]})

def parsed_message(raw_message: str):
    raw_message = raw_message.split(",")
    translation = Translator()
    translation = translation.translate(raw_message[0])
    codename = translation.text
    name = raw_message[0]
    if raw_message == "да" or "Да":
        is_base_expense = False
    else:
        is_base_expense = True
    aliases = []
    for i in raw_message[2:]:
        aliases.append(i)
    aliases = ",".join(aliases)
    return codename, name, is_base_expense,aliases

#add_category('здоровье, нет, лекарства, врач, диетолог')
def add_alias(cat: str, raw_message:str):
    category = cat
    raw_text = raw_message
    aliases = ", " + raw_text
    cursor = db.get_cursor()
    cursor.execute(f"UPDATE category SET aliases = CONCAT(aliases, '{aliases}') "
                     f"WHERE name = '{category}'")
    connection = db.connection
    connection.commit()



#add_alias('здоровье', 'туалетная бумага, анальгин')

#print(add_alias('здоровье', 'туалетная бумага, анальгин'))


