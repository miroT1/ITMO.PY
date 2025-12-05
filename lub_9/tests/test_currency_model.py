import unittest
from models.currency import Currency


class TestCurrencyModel(unittest.TestCase):

    def test_currency_creation(self) -> None:
        currency = Currency("840", "USD", "Доллар США", 90.0, 1)

        self.assertEqual(currency.num_code, "840")
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.name, "Доллар США")
        self.assertEqual(currency.value, 90.0)
        self.assertEqual(currency.nominal, 1)

    def test_char_code_setter_valid(self) -> None:
        currency = Currency("840", "USD", "Доллар США", 90.0, 1)

        currency.char_code = "EUR"
        self.assertEqual(currency.char_code, "EUR")
    def test_char_code_setter_invalid_length(self) -> None:
        currency = Currency("840", "USD", "Доллар США", 90.0, 1)

        with self.assertRaises(ValueError) as context:
            currency.char_code = "US"

        self.assertEqual(
            str(context.exception), "Код валюты должен состоять из 3 символов"
        )

    def test_char_code_setter_uppercase(self) -> None:
        currency = Currency("840", "USD", "Доллар США", 90.0, 1)

        currency.char_code = "eur"
        self.assertEqual(currency.char_code, "EUR")

    def test_value_setter_valid(self) -> None:
        currency = Currency("840", "USD", "Доллар США", 90.0, 1)

        currency.value = 95.5
        self.assertEqual(currency.value, 95.5)

    def test_value_setter_invalid_negative(self) -> None:
        currency = Currency("840", "USD", "Доллар США", 90.0, 1)

        with self.assertRaises(ValueError) as context:
            currency.value = -10.0

        self.assertEqual(
            str(context.exception), "Курс валюты не может быть отрицательным"
        )

    def test_read_only_properties(self) -> None:
        currency = Currency("840", "USD", "Доллар США", 90.0, 1)

        with self.assertRaises(AttributeError):
            currency.num_code = "978"

        with self.assertRaises(AttributeError):
            currency.name = "Евро"

        with self.assertRaises(AttributeError):
            currency.nominal = 10


if __name__ == "__main__":
    unittest.main()
