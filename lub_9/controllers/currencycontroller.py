from typing import List, Dict, Any
from models.currency import Currency
from controllers.databasecontroller import CurrencyRatesCRUD


class CurrencyController:
    def __init__(self, db_controller: CurrencyRatesCRUD) -> None:
        self.db = db_controller

    def list_currencies(self) -> List[Dict[str, Any]]:
        return self.db._read()

    def get_currency_by_char_code(self, char_code: str) -> List[Dict[str, Any]]:
        return self.db._read(char_code)

    def update_currency(self, char_code: str, value: float) -> None:
        if value < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        if len(char_code) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self.db._update({char_code.upper(): value})

    def delete_currency(self, currency_id: int) -> None:
        self.db._delete(currency_id)

    def create_currency(
        self, num_code: str, char_code: str, name: str, value: float, nominal: int
    ) -> None:
        try:
            currency_obj = Currency(num_code, char_code, name, value, nominal)
            currency_data = {
                "num_code": currency_obj.num_code,
                "char_code": currency_obj.char_code,
                "name": currency_obj.name,
                "value": currency_obj.value,
                "nominal": currency_obj.nominal,
            }
            self.db._create(currency_data)
        except ValueError as e:
            raise ValueError(f"Ошибка создания валюты: {e}")

    def get_user_currencies(self, user_id: int) -> List[Dict[str, Any]]:
        return self.db.get_user_currencies(user_id)