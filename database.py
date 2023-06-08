import sqlite3
import os


def create_database():
    # Подключаемся к базе данных
    conn = sqlite3.connect('example1.db')
    c = conn.cursor()
    # Создаем таблицу
    c.execute('''CREATE TABLE IF NOT EXISTS my_table
                 (col1 TEXT, col2 TEXT, col3 TEXT, col4 BOOLEAN)''')
    # Сохраняем изменения
    conn.commit()
    # Закрываем соединение
    conn.close()


def fill_data(list1, list2, string):
    # Подключаемся к базе данных
    conn = sqlite3.connect('example1.db')
    c = conn.cursor()
    # Заполняем таблицу данными
    for item1, item2 in zip(list1, list2):
        if item1 is None:
            col4_value = "False"
        else:
            col4_value = "True"
        if item1 is not None:
            item1 = os.path.splitext(os.path.basename(item1))[0]
        if item2 is not None:
            item2 = os.path.splitext(os.path.basename(item2))[0]
        c.execute("INSERT INTO my_table VALUES (?, ?, ?, ?)", (item1, item2, string, col4_value))
    # Сохраняем изменения
    conn.commit()
    # Закрываем соединение
    conn.close()


def view_data():
    # Подключаемся к базе данных
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Выполняем запрос для получения данных из таблицы
    c.execute("SELECT * FROM my_table")

    # Получаем все строки результата
    rows = c.fetchall()

    # Выводим содержимое таблицы
    for row in rows:
        print(row)

    # Закрываем соединение
    conn.close()
