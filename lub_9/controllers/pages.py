import os
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from models.author import Author


class PagesController:

    def __init__(self) -> None:
        templates_path = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(["html", "xml"]),
        )

        # Информация об авторе (из файла author.py)
        self.author = Author("Мирон", "P3124")

    def render_index(
        self,
        currencies: List[Dict[str, Any]],
        user_currencies: List[Dict[str, Any]] = None,) -> str:
        template = self.env.get_template("index.html")

        navigation = [
            {"caption": "Главная", "href": "/"},
            {"caption": "Об авторе", "href": "/author"},
            {"caption": "Пользователи", "href": "/users"},
            {"caption": "Валюты", "href": "/currencies"},
        ]

        return template.render(
            myapp="Currencies List App",
            navigation=navigation,
            author_name=self.author.name,
            author_group=self.author.group,
            currencies=currencies,
            user_currencies=user_currencies or [],
        )

    def render_author(self) -> str:
        template = self.env.get_template("author.html")
        return template.render(
            author_name=self.author.name, author_group=self.author.group
        )

    def render_users(self, users: List[Dict[str, Any]]) -> str:
        template = self.env.get_template("users.html")
        return template.render(users=users)

    def render_user(
        self, user: Dict[str, Any], currencies: List[Dict[str, Any]]) -> str:
        template = self.env.get_template("user.html")
        return template.render(user=user, currencies=currencies)

    def render_currencies(self, currencies: List[Dict[str, Any]]) -> str:
        template = self.env.get_template("currencies.html")
        return template.render(currencies=currencies)

    def render_message(self, message: str, title: str = "Сообщение") -> str:
        template = self.env.get_template("index.html")
        return template.render(
            myapp=title,
            navigation=[{"caption": "На главную", "href": "/"}],
            result=message,
        )
