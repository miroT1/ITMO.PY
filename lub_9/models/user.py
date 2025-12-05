class User:
    def __init__(self, name: str) -> None:
        self.__name = name.strip() if name else ""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, val: str) -> None:
        if not val or not val.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        self.__name = val.strip()
