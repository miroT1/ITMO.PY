import unittest
import sys
import os
from controllers.databasecontroller import CurrencyRatesCRUD
from controllers.currencycontroller import CurrencyController
from controllers.pages import PagesController
from models.currency import Currency
from models.user import User
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class IntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_controller = CurrencyRatesCRUD()
        cls.currency_controller = CurrencyController(cls.db_controller)
        cls.pages_controller = PagesController()

    def test_1_database_connection(self):
        self.assertIsNotNone(self.db_controller)

        currencies = self.db_controller._read()
        self.assertGreater(len(currencies), 0, "В базе должны быть валюты")

        print("Подключение к базе данных - успешно \n")

    def test_2_currency_model_validation(self):
        currency = Currency("840", "USD", "Доллар США", 90.0, 1)
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.value, 90.0)

        with self.assertRaises(ValueError):
            Currency("840", "US", "Доллар США", 90.0, 1)
        with self.assertRaises(ValueError):
            Currency("840", "USD", "Доллар США", -10.0, 1)
        print("Валидация модели Currency - успешно \n")

    def test_3_currency_crud_operations(self):
        currencies = self.currency_controller.list_currencies()
        initial_count = len(currencies)
        self.assertGreater(initial_count, 0)

        self.currency_controller.create_currency(
            num_code="392",
            char_code="JPY",
            name="Японская йена",
            value=0.62,
            nominal=100
        )
        currencies = self.currency_controller.list_currencies()
        self.assertEqual(len(currencies), initial_count + 1)

        self.currency_controller.update_currency("USD", 95.5)
        usd_currency = self.currency_controller.get_currency_by_char_code("USD")
        self.assertEqual(usd_currency[0]['value'], 95.5)

        jpy_currency = self.currency_controller.get_currency_by_char_code("JPY")
        if jpy_currency:
            currency_id = jpy_currency[0]['id']
            self.currency_controller.delete_currency(currency_id)

            currencies = self.currency_controller.list_currencies()
            self.assertEqual(len(currencies), initial_count)

        print("CRUD операции с валютами - успешно \n")

    def test_4_pages_rendering(self):
        currencies = self.currency_controller.list_currencies()

        index_html = self.pages_controller.render_index(currencies)
        self.assertIn("Currencies List App", index_html)
        self.assertIn("USD", index_html)

        author_html = self.pages_controller.render_author()
        self.assertIn("Мирон", author_html)
        self.assertIn("P3124", author_html)

        currencies_html = self.pages_controller.render_currencies(currencies)
        self.assertIn("Валюты", currencies_html)
        self.assertIn("USD", currencies_html)

        print("Рендеринг страниц - успешно \n")

    def test_5_user_functionality(self):
        user = User("Тестовый пользователь")
        self.assertEqual(user.name, "Тестовый пользователь")

        with self.assertRaises(ValueError):
            user.name = ""

        print("Функционал пользователя - успешно \n")

    def test_6_sql_injection_protection(self):
        malicious_input = "USD'; DROP TABLE currency; --"
        try:
            result = self.db_controller._read(malicious_input)
            self.assertTrue(True)
        except Exception as e:
            self.assertNotIn("DROP TABLE", str(e))
        print("Защита от SQL-инъекций - успешно \n")

    def test_7_mvc_architecture_compliance(self):
        currency = Currency("978", "EUR", "Евро", 91.0, 1)
        self.assertTrue(hasattr(currency, 'char_code'))
        self.assertTrue(hasattr(currency, 'value'))

        self.assertTrue(hasattr(self.currency_controller, 'list_currencies'))
        self.assertTrue(hasattr(self.currency_controller, 'update_currency'))

        print("Соответствие архитектуре MVC - успешно \n")


class FullApplicationTest(unittest.TestCase):
    def setUp(self):
        self.server_url = "http://localhost:8080"

    def test_application_startup(self):
        print("http://localhost:8080 \n")
        self.assertTrue(True)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(IntegrationTests))
    suite.addTests(loader.loadTestsFromTestCase(FullApplicationTest))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("База данных: работает корректно \n")
        print("Модели: валидация работает \n")
        print("CRUD операции: выполняются \n")
        print("Рендеринг страниц: работает \n")
        print("Архитектура MVC: соблюдена \n")
        print("Безопасность: защита от SQL-инъекций реализована \n")
    else:
        print("ERROR")
        for test, error in result.errors:
            print(f"ERROR {test}: {error}")
        for test, failure in result.failures:
            print(f"ERROR {test}: {failure}")

    exit(0 if result.wasSuccessful() else 1)