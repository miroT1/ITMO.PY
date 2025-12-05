Цель работы - создать веб приложение для взаимодействия с курсами и пользователями с полной реализацией CRUD-операций, использованием SQLite в памяти

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






  
