import functools
import io
import logging
import sys
import unittest
from typing import Optional, Union
import requests
from requests.exceptions import RequestException


def logger(output: Optional[Union[logging.Logger, io.TextIOBase]] = None):
    if output is None:
        output = sys.stdout

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(output, logging.Logger):
                log_info = output.info
                log_error = output.error
            else:
                def log_to_stream(level, message):
                    output.write(f"{level}: {message}\n")
                    if hasattr(output, 'flush'):
                        output.flush()
                log_info = lambda msg: log_to_stream("INF", msg)
                log_error = lambda msg: log_to_stream("ERROR", msg)

            func_name = func.__name__
            log_info(f"Вызываем '{func_name}' с аргументами: {args}, {kwargs}")

            try:
                result = func(*args, **kwargs)
                log_info(f"'{func_name}' успешно завершилась, результат: {result}")
                return result
            except Exception as e:
                error_msg = f"'{func_name}' вызвала исключение {type(e).__name__}: {str(e)}"
                log_error(error_msg)
                raise

        return wrapper

    return decorator


def get_currencies(codes: list, api_url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        raise ConnectionError(f"Нет подключения к API: {e}")

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError("Данные не в формате JSON") from e

    if "Valute" not in data:
        raise KeyError("В ответе отсутствует ключ 'Valute'")
    currencies = data["Valute"]
    rates = {}

    for code in codes:
        if code not in currencies:
            raise KeyError(f"{code} не найден")
        try:
            rate = float(currencies[code]["Value"])
            rates[code] = round(rate, 2)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Ошибка в значении {code}") from e
    return rates


@logger()
def get_currency_rates_with_logging(codes: list) -> dict:
    return get_currencies(codes)



@logger()
def solve_quadratic_equation(a: float, b: float, c: float) -> tuple:

    if not all(isinstance(coef, (int, float)) for coef in (a, b, c)):
        raise TypeError("Некорректные данные")

    if a == 0:
        if b == 0:
            raise ValueError("Коофиценты нулевые")
        return (-c / b,)
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return ()
    elif discriminant == 0:
        root = -b / (2 * a)
        return (root,)
    else:
        sqrt_discriminant = discriminant ** 0.5
        root1 = (-b + sqrt_discriminant) / (2 * a)
        root2 = (-b - sqrt_discriminant) / (2 * a)
        return root1, root2



class TestGetCurrencies(unittest.TestCase):
    def test_gets_rates_for_multiple_currencies(self):
        rates = get_currencies(['USD', 'EUR'])
        self.assertIsInstance(rates, dict)
        self.assertIn('USD', rates)
        self.assertIn('EUR', rates)
        self.assertIsInstance(rates['USD'], float)

    def test_raises_error_for_invalid_currency(self):
        with self.assertRaises(KeyError):
            get_currencies(['NONEXISTENT'])


class LoggingDecoratorTests(unittest.TestCase):
    def setUp(self):
        self.log_output = io.StringIO()
    def test_logs_successful_execution(self):
        @logger(self.log_output)
        def multiply_by_two(x):
            return x * 2
        result = multiply_by_two(7)
        logs = self.log_output.getvalue()
        self.assertEqual(result, 14)
        self.assertIn("Вызываем 'multiply_by_two'", logs)
        self.assertIn("успешно завершилась", logs)

    def test_logs_errors_correctly(self):
        @logger(self.log_output)
        def failing_function():
            raise RuntimeError("Что-то пошло не так")
        with self.assertRaises(RuntimeError):
            failing_function()
        logs = self.log_output.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("RuntimeError", logs)


class TestStreamWrite(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()
        @logger(self.stream)
        def wrapped():
            return get_currencies(['USD'], api_url="https://invalid")
        self.wrapped = wrapped
    def test_logging_error(self):
        with self.assertRaises(ConnectionError):
            self.wrapped()
        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)


def show_examples():
    print("\n1. курсы валют с логированием:")
    try:
        rates = get_currency_rates_with_logging(['USD'])
        print(f"Текущий курс USD: {rates['USD']} руб.")
    except Exception as e:
        print(f"Ошибка: {e}")
    print("\n2. квадратные уравнения:")

    roots = solve_quadratic_equation(1, -5, 6)
    print(f"Уравнение x² - 5x + 6 = 0, корни: {roots}")

    # Пример без корней
    roots = solve_quadratic_equation(1, 0, 1)
    print(f"Уравнение x² + 1 = 0, корни: {roots}")

    try:
        solve_quadratic_equation(0, 0, 5)
    except ValueError as e:
        print(f"Ошибка при решении: {e}")
    print("\n3. Логирование в разные места:")
    print("-" * 40)

    file_logger = logging.getLogger("app")
    file_logger.setLevel(logging.INFO)

    file_logger.handlers.clear()

    handler = logging.FileHandler("app.log", mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    file_logger.addHandler(handler)

    @logger(file_logger)
    def example_function(value):
        return value * 3
    example_function(10)
    print("Логи записаны в файл app.log")


def run_all_tests():

    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(test_loader.loadTestsFromTestCase(TestGetCurrencies))
    test_suite.addTests(test_loader.loadTestsFromTestCase(LoggingDecoratorTests))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestStreamWrite))

    test_runner = unittest.TextTestRunner(verbosity=2)
    results = test_runner.run(test_suite)

    return results


if __name__ == "__main__":
    show_examples()
    run_all_tests()