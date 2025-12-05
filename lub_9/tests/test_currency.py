import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController


class TestCurrencyController(unittest.TestCase):
    def test_list_currencies(self) -> None:
        mock_db = MagicMock()
        mock_db._read.return_value = [
            {"id": 1, "char_code": "USD", "value": 90.0},
            {"id": 2, "char_code": "EUR", "value": 91.0},
        ]
        controller = CurrencyController(mock_db)
        result = controller.list_currencies()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["char_code"], "USD")
        self.assertEqual(result[0]["value"], 90.0)
        mock_db._read.assert_called_once()

    def test_update_currency_success(self) -> None:
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)
        controller.update_currency("USD", 95.5)
        mock_db._update.assert_called_once_with({"USD": 95.5})

    def test_update_currency_validation_error(self) -> None:
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)

        with self.assertRaises(ValueError) as context:
            controller.update_currency("USD", -10.0)

        self.assertEqual(
            str(context.exception), "Курс валюты не может быть отрицательным"
        )

        mock_db._update.assert_not_called()

    def test_update_currency_code_validation(self) -> None:
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)

        with self.assertRaises(ValueError) as context:
            controller.update_currency("US", 95.5)

        self.assertEqual(
            str(context.exception), "Код валюты должен состоять из 3 символов"
        )

        mock_db._update.assert_not_called()

    def test_delete_currency(self) -> None:
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)
        controller.delete_currency(1)
        mock_db._delete.assert_called_once_with(1)

    def test_get_currency_by_char_code(self) -> None:
        mock_db = MagicMock()
        mock_db._read.return_value = [{"id": 1, "char_code": "USD", "value": 95.5}]

        controller = CurrencyController(mock_db)

        result = controller.get_currency_by_char_code("USD")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["char_code"], "USD")

        mock_db._read.assert_called_once_with("USD")

    def test_create_currency_success(self) -> None:

        mock_db = MagicMock()
        controller = CurrencyController(mock_db)

        controller.create_currency(
            num_code="392",
            char_code="JPY",
            name="Японская йена",
            value=0.62,
            nominal=100,
        )

        mock_db._create.assert_called_once()

        call_args = mock_db._create.call_args[0][0]
        self.assertEqual(call_args["num_code"], "392")
        self.assertEqual(call_args["char_code"], "JPY")
        self.assertEqual(call_args["name"], "Японская йена")
        self.assertEqual(call_args["value"], 0.62)
        self.assertEqual(call_args["nominal"], 100)

    def test_create_currency_validation_error(self) -> None:
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)
        with self.assertRaises(ValueError) as context:
            controller.create_currency(
                num_code="392",
                char_code="JPY",
                name="Японская йена",
                value=-0.62,
                nominal=100,
            )
        self.assertIn("Курс валюты не может быть отрицательным", str(context.exception))
        mock_db._create.assert_not_called()

    def test_get_user_currencies(self) -> None:
        mock_db = MagicMock()
        mock_db.get_user_currencies.return_value = [
            {"id": 1, "char_code": "USD", "value": 95.5},
            {"id": 2, "char_code": "EUR", "value": 91.0},
        ]
        controller = CurrencyController(mock_db)
        result = controller.get_user_currencies(1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["char_code"], "USD")
        mock_db.get_user_currencies.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
