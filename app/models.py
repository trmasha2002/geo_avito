import sqlite3

import uuid
from hashlib import sha256


class Database:
    def __init__(self, databaseName):
        self._conn = sqlite3.connect(databaseName, check_same_thread=False)
        self._cursor = self._conn.cursor()

    def add_table_users(self):
        try:
            self._cursor.execute(
                """ CREATE TABLE IF NOT EXISTS users (
                login text,
                password text,
                token text
            )
            """
            )
        except ConnectionError as e:
            print(e)
        self._conn.commit()

    def add_user(self, login, password):
        token = str(uuid.uuid4().hex)
        password = sha256(str(password).encode('utf-8')).hexdigest()
        try:
            self._cursor.executemany(
                """
                INSERT INTO users (login, password, token) VALUES (?, ?, ?)
            """,
                [(login, password, token)])
        except Exception as e:
            print(e)
        self._conn.commit()

    def get_token_by_login_and_password(self, login, password):
        password = sha256(str(password).encode('utf-8')).hexdigest()
        print("blabla", login, password)
        try:
            self._cursor.execute(
                """
                SELECT token FROM users WHERE login = (?) AND password = (?)
            """, (login, password))
        except Exception as e:
            print(e)
        else:
            self._conn.commit()
            result = self._cursor.fetchone()
            if result is None:
                return None
            else:
                return result[0]



