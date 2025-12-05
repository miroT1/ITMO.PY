import sqlite3
from typing import List, Dict, Optional, Any


class CurrencyRatesCRUD:


    def __init__(self) -> None:
        self.__con = sqlite3.connect(":memory:")
        self.__cursor = self.__con.cursor()
        self.__create_tables()
        self.__insert_initial_data()

    def __create_tables(self) -> None:
        self.__con.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )
        self.__con.execute(
            """
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            )
            """
        )
        self.__con.execute(
            """
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            )
            """
        )
        self.__con.commit()

    def __insert_initial_data(self) -> None:
        users = [
            {"name": "Быстров Николай"},
            {"name": "Рябков Александр"},
            {"name": "Алабердин Артем"},
        ]
        sql_users = "INSERT INTO user(name) VALUES(:name)"
        self.__cursor.executemany(sql_users, users)

        currencies = [
            {
                "num_code": "840",
                "char_code": "USD",
                "name": "Доллар США",
                "value": 90.0,
                "nominal": 1,
            },
            {
                "num_code": "978",
                "char_code": "EUR",
                "name": "Евро",
                "value": 91.0,
                "nominal": 1,
            },
            {
                "num_code": "826",
                "char_code": "GBP",
                "name": "Фунт стерлингов",
                "value": 100.0,
                "nominal": 1,
            },
            {
                "num_code": "036",
                "char_code": "AUD",
                "name": "Австралийский доллар",
                "value": 52.8501,
                "nominal": 1,
            },
        ]
        sql_currencies = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        self.__cursor.executemany(sql_currencies, currencies)

        user_currency_links = [
            {"user_id": 1, "currency_id": 1},  # Иван следит за USD
            {"user_id": 1, "currency_id": 2},  # Иван следит за EUR
            {"user_id": 2, "currency_id": 1},  # Петр следит за USD
            {"user_id": 3, "currency_id": 3},  # Мария следит за GBP
        ]
        sql_links = """
            INSERT INTO user_currency(user_id, currency_id) 
            VALUES(:user_id, :currency_id)
        """
        self.__cursor.executemany(sql_links, user_currency_links)

        self.__con.commit()

    def _create(self, currency_data: Dict[str, Any]) -> None:
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        self.__cursor.execute(sql, currency_data)
        self.__con.commit()

    def _read(self, char_code: Optional[str] = None) -> List[Dict[str, Any]]:
        if char_code:
            sql = "SELECT * FROM currency WHERE char_code = ?"
            self.__cursor.execute(sql, (char_code,))
        else:
            sql = "SELECT * FROM currency"
            self.__cursor.execute(sql)

        result_data = []
        for row in self.__cursor.fetchall():
            _d = {
                "id": int(row[0]),
                "num_code": row[1],
                "char_code": row[2],
                "name": row[3],
                "value": float(row[4]),
                "nominal": int(row[5]),
            }
            result_data.append(_d)

        return result_data

    def _update(self, currency_data: Dict[str, float]) -> None:
        if not currency_data:
            return

        char_code = list(currency_data.keys())[0]
        new_value = currency_data[char_code]

        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        self.__cursor.execute(sql, (new_value, char_code))
        self.__con.commit()

    def _delete(self, currency_id: int) -> None:
        sql_delete_links = "DELETE FROM user_currency WHERE currency_id = ?"
        self.__cursor.execute(sql_delete_links, (currency_id,))
        sql_delete_currency = "DELETE FROM currency WHERE id = ?"
        self.__cursor.execute(sql_delete_currency, (currency_id,))
        self.__con.commit()

    def get_user_currencies(self, user_id: int) -> List[Dict[str, Any]]:
        sql = """
            SELECT c.* 
            FROM currency c
            JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        """
        self.__cursor.execute(sql, (user_id,))

        result_data = []
        for row in self.__cursor.fetchall():
            _d = {
                "id": int(row[0]),
                "num_code": row[1],
                "char_code": row[2],
                "name": row[3],
                "value": float(row[4]),
                "nominal": int(row[5]),
            }
            result_data.append(_d)
        return result_data

    def __del__(self) -> None:
        try:
            if hasattr(self, "_CurrencyRatesCRUD__con") and self.__con:
                self.__con.close()
        except (AttributeError, sqlite3.ProgrammingError):
            pass
