Цель работы - создать веб приложение для взаимодействия с курсами и пользователями с полной реализацией CRUD-операций, использованием SQLite в памяти\



Описание моделей
Currency:
* num_code - код валюты
* char_code - буквенный код (3 символа, использование валидации)
* name - название валюты
* value - курс
* nominal - номинал
User:
* name - имя пользователя
Author:
* name - имя автора
* group - номер группы
  


Структура проекта

        lub_9
          controllers
            __init__.py
            currencycontroller.py
            databasecontroller.py
            pages.py
          models
            __init__.py
            author.py
            currency.py
            user.py
          templates
            author.html
            currencies.html
            index.html
            user.html
            users.html
          tests/
          myapp.py



Реализация CRUD с примерами SQL-запросов

Create

    INSERT INTO currency(num_code, char_code, name, value, nominal) 
    VALUES(:num_code, :char_code, :name, :value, :nominal)

read

    SELECT * FROM currency
    SELECT * FROM currency WHERE char_code = ?
    SELECT c.* FROM currency c JOIN user_currency uc ON c.id = uc.currency_id WHERE uc.user_id = ?

update

    UPDATE currency SET value = ? WHERE char_code = ?

delete

    DELETE FROM user_currency WHERE currency_id = ?
    DELETE FROM currency WHERE id = ?



Скриншоты работы приложения

Главная страница

<img width="2559" height="1402" alt="image" src="https://github.com/user-attachments/assets/c30a19a8-48da-4cda-b5ef-e614dbc54d97" />

Таблица валют

<img width="2559" height="1395" alt="image" src="https://github.com/user-attachments/assets/5589ead2-729c-4cfe-b59f-c2610a35b997" />

Пользователи

<img width="2559" height="1396" alt="image" src="https://github.com/user-attachments/assets/6d49f351-9da0-4a57-9289-84aab88a8a53" />




Примеры тестов с unittest.mock и результаты их выполнения

Тест CurrencyController:

        def test_list_currencies(self):
            mock_db = MagicMock()
            mock_db._read.return_value = [
                {"id": 1, "char_code": "USD", "value": 90.0}
            ]
            controller = CurrencyController(mock_db)
            result = controller.list_currencies()
            self.assertEqual(result[0]['char_code'], "USD")
            mock_db._read.assert_called_once()
        
        def test_update_currency_validation_error(self):
            mock_db = MagicMock()
            controller = CurrencyController(mock_db)
            with self.assertRaises(ValueError) as context:
                controller.update_currency("USD", -10.0)
            self.assertEqual(
                str(context.exception), 
                "Курс валюты не может быть отрицательным"
            )
            mock_db._update.assert_not_called()
    
Результаты выполнения:

    test_create_currency_success ... ok
    test_create_currency_validation_error ... ok
    test_delete_currency ... ok
    test_get_currency_by_char_code ... ok
    test_get_user_currencies ... ok
    test_list_currencies ... ok
    test_update_currency_code_validation ... ok
    test_update_currency_success ... ok
    test_update_currency_validation_error ... ok
    ----------------------------------------------------------------------
    Ran 9 tests in 0.002s
    OK



Выводы:

Применение MVC:

* Четкое разделение ответственности между компонентами

* Модели содержат только данные и валидацию

* Контроллеры реализуют бизнес-логику

* Представления отвечают только за отображение

* Упрощена поддержка и тестирование кода

Работа с SQLite:

* Первичные ключи обеспечили уникальность записей

* Внешние ключи гарантировали целостность данных

* Параметризованные запросы исключили SQL-инъекции

Обработка маршрутов:

* Реализован полноценный роутер для GET-запросов

* Каждый маршрут делегирует выполнение соответствующему контроллеру

* Поддерживаются все требуемые эндпоинты

* Обработка query-параметров для фильтрации и действий

Рендеринг шаблонов:

* Jinja2 эффективно разделил логику и представление

* Bootstrap использован для стилизации интерфейса\

* Шаблоны поддерживают динамическое отображение данных

* Обеспечена безопасность через экранирование HTML
