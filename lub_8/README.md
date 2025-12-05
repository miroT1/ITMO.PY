ОТЧЕТ О 8 ЛАБОРАТОРНОЙ РАБОТЕ

Цель работы - создание клиент-серверного веб приложения для просмотра курсов валют и использованием архитектуры MVC.

В работе выполнены задачи:

1 Реализация моделей с геттерами и сеттерами

2 Создание HTTP сервера с маршрутизацией

3 Использование Jinja2 для отображение данных

4 Использоване курсов валют через API Центрального банка России

5 Тестирование для корректной работы



Модели данных:

1 Author - Автор приложения

    name - имя автора
    group - номер группы
	
	
2 App - приложение

    name - название
    author - автор
    version - версия
	
3 User - пользователь

    id - идентификатор
	name - имя пользователя
	
4 Currency - валюта

	id - идентификатор
	name - название валюты
	num_code - код из цифр
	char_code - код из символов
	value - курс

5 UserCurrency - подписка пользователя

	id - идентификатор
	user_id - внешний ключ к пользователю
	currently_if - внешний ключ к валюте



Структура проекта

	lub8
		models
			__init__.py - экспорт всех моделей
			author.py - класс Author
			app.py - класс App
			currency.py - класс Currency
			user.py - класс User
			user_currency.py - класс UserCurrency
		templates
			author.html - страница об авторе
			currencies.html - список валют
			index.html - Главное меню
			user.html - страница пользователя
			users.html - список пользователей
		utils
			currencies_api.py - функции работы с API валют
		myapp.py - Основной файл


Описание реализации

1 Реализация моделей и их свойства

	class User:
	    def __init__(self, id: int, name: str):
	        self.__id: int = None
	        self.__name: str = None
	        self.id = id #использование сеттора для валидации
	        self.name = name
	    @property
	    def id(self):
	        return self.__id
	    @id.setter
	    def id(self, id: int):
	        if type(id) is int and id > 0:
	            self.__id = id
	        else:
	            raise ValueError('ERROR')


2 Реализация маршрутов и обработка запросов

	class CurrencyRequestHandler(BaseHTTPRequestHandler):
	    def do_GET(self):
	        parsed_url = urlparse(self.path)
	        path = parsed_url.path
	        query_params = parse_qs(parsed_url.query)
	        if path == '/':
	            '''Обработка главной страницы'''
	        elif path == '/users':
	            '''Обработка списка пользователей'''
	        elif path == '/user':
	            '''Обработка страницы пользователя'''
	            user_id = query_params.get('id', [''])[0]
	        ''' другие маршруты'''


3 Использование шаблонизатора Jinja2 

	from jinja2 import Environment, PackageLoader, select_autoescape
	
	env = Environment(
	    loader=PackageLoader("myapp"),  # Загрузчик для пакета myapp
	    autoescape=select_autoescape()   # Автоматическое экранирование HTML
	)

* Environment хранится в глобальной переменной для повторного использования
* PackageLoader загружает шаблоны из папки templates/ пакета myapp

4 Интеграция функции get_currencies для получения актуальных курсов

	def get_currency_details() -> List[Dict]:
	    try:
	        url = "https://www.cbr-xml-daily.ru/daily_json.js"
	        response = requests.get(url, timeout=10)
	        response.raise_for_status()
	        data = response.json()
	        currencies_data = data.get('Valute', {})
	        result = []
	        for code, info in currencies_data.items():
	            result.append({
	                'id': info['ID'],
	                'num_code': str(info['NumCode']),
	                'char_code': info['CharCode'],
	                'name': info['Name'],
	                'value': str(info['Value']).replace('.', ','),
	                'nominal': info['Nominal']
	            })
	        return result


Примеры задания 

Главная страница
<img width="2559" height="1399" alt="image" src="https://github.com/user-attachments/assets/4939040a-8213-432a-b59f-6f5d8b5e8f3f" />

Список пользователей
<img width="2559" height="1394" alt="image" src="https://github.com/user-attachments/assets/ef9a96b2-d57b-406f-9f66-aaf34720cc50" />

Страница пользователя
<img width="2559" height="1401" alt="image" src="https://github.com/user-attachments/assets/ac4ec9e9-aefe-42fc-b148-dfd2193744ae" />

Список валют
<img width="2538" height="1395" alt="image" src="https://github.com/user-attachments/assets/8cb50a50-195f-4d9a-995d-b2b11ebeb64e" />

Страница об авторе
<img width="2559" height="1401" alt="image" src="https://github.com/user-attachments/assets/1a86a651-8331-4776-a170-71a87c56f1e5" />


Тестирование

1 Тестирование моделей

	def test_user_creation_valid(self):
	    """Тест создания пользователя с валидными данными"""
	    user = User(1, "Иван Иванов")
	    self.assertEqual(user.id, 1)
	    self.assertEqual(user.name, "Иван Иванов")
	
	def test_user_id_validation(self):
	    """Тест валидации ID пользователя"""
	    user = User(1, "Иван Иванов")
	    '''Корректный ID'''
	    user.id = 100
	    self.assertEqual(user.id, 100)
	    '''Некорректный ID - отрицательный'''
	    with self.assertRaises(ValueError):
	        user.id = -1

2 Тестирование функции get_currencies

	@patch('utils.currencies_api.requests.get')
	def test_get_currencies_success(self, mock_get):
	    mock_response = Mock()
	    mock_response.status_code = 200
	    mock_response.json.return_value = {
	        'Valute': {
	            'USD': {
	                'ID': 'R01235',
	                'NumCode': '840',
	                'CharCode': 'USD',
	                'Nominal': 1,
	                'Name': 'Доллар США',
	                'Value': 91.2345
	            }
	        }
	    }
	    mock_get.return_value = mock_response
	    currencies = get_currencies(['USD'])
	    self.assertIn('USD', currencies)
	    self.assertEqual(str(currencies['USD']), '91.2345')

3 Тестирование контроллера

	def test_handle_index(self):
	    self.handler._handle_index()
	    self.assertEqual(self.handler.response_code, 200)
	    self.assertIn('CurrenciesListApp', self.handler._get_response_content())
	
	def test_handle_user_detail_valid(self):
	    from myapp import CurrencyRequestHandler
	    handler = MockHandler()
	    handler._handle_user_detail('1')

Результаты тестирования

	test_user_creation_valid ... ok
	test_user_id_validation ... ok
	test_get_currencies_success ... ok
	test_handle_index ... ok
	test_handle_users ... ok


Выводы

Проблемы при реализации:

1 Валидация данных - требовалась корректировка проверок входных параметров в сеттерах моделей
2 Обработка запросов - необходимость самостоятельной реализации парсинга URL и query-параметров
3 Интеграция внешнего API - обработка неоднородных форматов данных
4 Конфигурация шаблонизатора - настройка корректных путей для загрузки шаблонов

Реализация архитектуры MVC

1 Применение архитектурного паттерна Model-View-Controller позволило:
2 Четко разделить ответственность между компонентами приложения
3 Обеспечить модульность и поддерживаемость кода
4 Упростить тестирование отдельных компонентов системы
5 Модели содержат бизнес-логику, представления отвечают за отображение данных, контроллер осуществляет координацию между ними.

Приобретенный опыт

В результате выполнения работы были получены практические навыки:
1 Разработка HTTP-серверов на базе стандартных библиотек Python
2 Использование шаблонизатора Jinja2 для динамической генерации веб-страниц
3 Интеграция внешних API с обработкой исключительных ситуаций
4 Реализация MVC-архитектуры в клиент-серверных приложениях
