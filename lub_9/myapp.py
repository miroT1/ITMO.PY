from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from controllers.databasecontroller import CurrencyRatesCRUD
from controllers.currencycontroller import CurrencyController
from controllers.pages import PagesController


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        print(f"Запрос: {path}, Параметры: {query_params}")

        if path == "/":
            currencies = currency_controller.list_currencies()
            user_currencies = currency_controller.get_user_currencies(1)
            html = pages_controller.render_index(currencies, user_currencies)
            self._send_response(html)

        elif path == "/author":
            html = pages_controller.render_author()
            self._send_response(html)

        elif path == "/users":
            users = [
                {"id": 1, "name": "Быстров Николай"},
                {"id": 2, "name": "Рябков Александр"},
                {"id": 3, "name": "Алабердин Артем"},
            ]
            html = pages_controller.render_users(users)
            self._send_response(html)

        elif path == "/user":
            if "id" in query_params:
                user_id = int(query_params["id"][0])
                user = {"id": user_id, "name": f"Пользователь {user_id}"}
                currencies = currency_controller.get_user_currencies(user_id)
                html = pages_controller.render_user(user, currencies)
                self._send_response(html)
            else:
                self._send_error("Не указан ID пользователя")

        elif path == "/currencies":
            currencies = currency_controller.list_currencies()
            html = pages_controller.render_currencies(currencies)
            self._send_response(html)

        elif path == "/currency/delete":
            if "id" in query_params:
                currency_id = int(query_params["id"][0])
                currency_controller.delete_currency(currency_id)
                html = pages_controller.render_message(
                    f"Валюта с ID {currency_id} удалена", "Удаление валюты"
                )
                self._send_response(html)
            else:
                self._send_error("Не указан ID валюты для удаления")

        elif path == "/currency/update":
            updated = False
            for param, values in query_params.items():
                if param.upper() in ["USD", "EUR", "GBP", "AUD"]:
                    try:
                        new_value = float(values[0])
                        currency_controller.update_currency(
                            param.upper(), new_value
                        )
                        updated = True
                    except ValueError as e:
                        self._send_error(f"Ошибка обновления: {e}")
                        return

            if updated:
                html = pages_controller.render_message(
                    "Курсы валют обновлены", "Обновление курсов"
                )
                self._send_response(html)
            else:
                self._send_error("Не указаны валюты для обновления")

        elif path == "/currency/show":
            currencies = currency_controller.list_currencies()
            print("Текущие курсы валют:")
            for currency in currencies:
                print(f"{currency['char_code']}: {currency['value']}")
            html = pages_controller.render_message(
                "Курсы валют выведены в консоль", "Отладочная информация"
            )
            self._send_response(html)

        else:
            self._send_error("Страница не найдена", 404)

    def _send_response(self, html: str, status_code: int = 200) -> None:
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _send_error(self, message: str, status_code: int = 400) -> None:
        html = f"""
        <html>
            <head><title>Ошибка {status_code}</title></head>
            <body>
                <h1>Ошибка {status_code}</h1>
                <p>{message}</p>
                <a href="/">На главную</a>
            </body>
        </html>
        """
        self._send_response(html, status_code)


def main() -> None:
    global currency_controller, pages_controller
    db_controller = CurrencyRatesCRUD()
    currency_controller = CurrencyController(db_controller)
    pages_controller = PagesController()

    server_address = ("localhost", 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Сервер запущен на http://{server_address[0]}:{server_address[1]}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()