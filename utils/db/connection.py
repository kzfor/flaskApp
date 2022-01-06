"""
Класс написал для того, чтобы работа с БД была завязана не на sqlite, а на "какой-то" БД
Например, если захочешь накатить постгрес, вместо замены кода в 100 местах, просто переписываешь утилитарный класс
Тут я сделал это не совсем правильно т.к. я не "обернул" курсор и сам коннекшн в свои классы, и приложение
все равно зависит от API Sqlite (закрытие курсора/соединения).
То есть, если я сменю коннектор, и он будет коммитить изменения не через get_cursor().commit() а через get_cursor().apply(),
то все сломается.
"""

import sqlite3

class DatabaseConnection:
    def __init__(self):
        # Создаем коннект к БД
        try:
            self.connection = sqlite3.connect('data.db', check_same_thread=False)
            self.connection.execute("PRAGMA foreign_keys = ON;")
        except Exception as e:
            print(f'Не удалось соединиться с БД {str(e)}')

    def get_cursor(self):
        # Получаем инстанс курсора для выполнения SQL
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()
    