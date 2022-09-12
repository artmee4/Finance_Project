import psycopg2
from psycopg2 import Error
from psycopg2 import OperationalError
from typing import Dict, List, Tuple

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

    # Подключение к существующей базе данных
connection = psycopg2.connect("dbname='telegbotdb1' user='postgres' password='123' host='localhost' port='5432'")
cursor = connection.cursor()
# Курсор для выполнения операций с базой данных


def insert(table: str, column_values: Dict):
    conn=psycopg2.connect("dbname='telegbotdb1' user='postgres' password='123' host='localhost' port='5432'")
    cursor = conn.cursor()
    columns = ', '.join(column_values.keys())
    values = list(column_values.values())
    placeholders = ', '.join( ['%s'] * len(column_values))
    sql = " INSERT INTO %s ( %s ) VALUES ( %s ) " % (table, columns, placeholders)
    cursor.execute(sql, values)
    conn.commit()


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


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    connection.commit()

def check_connection():
    cursor.execute("""SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'""")
    for table in cursor.fetchall():
        print(table)

def get_cursor():
    return cursor