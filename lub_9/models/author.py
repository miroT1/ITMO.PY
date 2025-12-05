class Author:

    def __init__(self, name: str, group: str) -> None:
        self.__name: str = name
        self.__group: str = group

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError("Ошибка при задании имени автора")

    @property
    def group(self) -> str:
        return self.__group

    @group.setter
    def group(self, group: str) -> None:
        if isinstance(group, str) and len(group) > 5:
            self.__group = group
        else:
            raise ValueError("Ошибка при задании группы автора")
