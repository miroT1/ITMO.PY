from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currency_details


env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)


main_author = Author('Мирон', 'p3124')
main_app = App('CurrenciesListApp', '1.0.0', main_author)
users = [
    User(1, 'AR'),
    User(2, 'Николай Быстров'),
    User(3, 'Артем')
]


currencies_data = get_currency_details()
currencies = []
for data in currencies_data:
    currencies.append(Currency(
        id=data['id'],
        num_code=data['num_code'],
        char_code=data['char_code'],
        name=data['name'],
        value=data['value'],
        nominal=data['nominal']
    ))



subscriptions = [
    UserCurrency(1, 1, currencies[0].id if currencies else ''),
    UserCurrency(2, 1, currencies[1].id if len(currencies) > 1 else ''),
    UserCurrency(3, 2, currencies[0].id if currencies else '')
]


class CurrencyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Главная страница
        if path == '/':
            template = env.get_template("index.html")
            html = template.render(
                myapp=main_app.name,
                author_name=main_author.name,
                group=main_author.group
            )
            self._send_html(html)

        # Список пользователей
        elif path == '/users':
            template = env.get_template("users.html")
            html = template.render(
                users=users,
                author_name=main_author.name,
                author_group=main_author.group
            )
            self._send_html(html)

        # Страница конкретного пользователя
        elif path == '/user':
            user_id = query_params.get('id', [''])[0]
            if user_id and user_id.isdigit():
                user_id = int(user_id)
                user = next((u for u in users if u.id == user_id), None)

                if user:
                    # Находим подписки пользователя
                    user_subscriptions = []
                    for sub in subscriptions:
                        if sub.user_id == user_id:
                            # Находим валюту по ID
                            currency = next((c for c in currencies if c.id == sub.currency_id), None)
                            if currency:
                                user_subscriptions.append({
                                    'id': sub.id,
                                    'currency': currency
                                })

                    template = env.get_template("user.html")
                    html = template.render(
                        user=user,
                        subscriptions=user_subscriptions,
                        author_name=main_author.name,
                        author_group=main_author.group
                    )
                    self._send_html(html)
                else:
                    self.send_error(404, "Пользователь не найден")
            else:
                self.send_error(400, "Не указан или некорректный ID пользователя")

        # Список валют
        elif path == '/currencies':
            # Проверяем, нужно ли обновить курсы
            refresh = query_params.get('refresh', [''])[0] == 'true'

            if refresh:
                # Обновляем данные о валютах
                currencies.clear()
                new_data = get_currency_details()
                for data in new_data:
                    currencies.append(Currency(
                        id=data['id'],
                        num_code=data['num_code'],
                        char_code=data['char_code'],
                        name=data['name'],
                        value=data['value'],
                        nominal=data['nominal']
                    ))

            template = env.get_template("currencies.html")
            html = template.render(
                currencies=currencies,
                author_name=main_author.name,
                author_group=main_author.group
            )
            self._send_html(html)

        # Страница об авторе
        elif path == '/author':
            template = env.get_template("author.html")
            html = template.render(
                author_name=main_author.name,
                author_group=main_author.group,
                app_name=main_app.name,
                app_version=main_app.version
            )
            self._send_html(html)

        # Неизвестный маршрут
        else:
            self.send_error(404, "Страница не найдена")

    def _send_html(self, html_content: str):
        """Отправка HTML-ответа"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def log_message(self, format, *args):
        """Переопределение логирования для красивого вывода"""
        print(f"[{self.client_address[0]}] {args[0]}")


if __name__ == '__main__':
    # Запуск сервера
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, CurrencyRequestHandler)



    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")