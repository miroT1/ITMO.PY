class Currency:
    def __init__(self, id: str, num_code: str, char_code: str,
                 name: str, value: str, nominal: int):
        self.__id: str = None
        self.__num_code: str = None
        self.__char_code: str = None
        self.__name: str = None
        self.__value: str = None
        self.__nominal: int = None

        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if type(id) is str and len(id) > 0:
            self.__id = id
        else:
            raise ValueError('ERROR')

    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: str):
        if type(num_code) is str and len(num_code) == 3 and num_code.isdigit():
            self.__num_code = num_code
        else:
            raise ValueError('ERROR')

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        if type(char_code) is str and len(char_code) == 3:
            self.__char_code = char_code
        else:
            raise ValueError('ERROR')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('ERROR')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if type(value) is str and len(value) > 0:
            # Заменяем точку на запятую для единообразия
            self.__value = value.replace('.', ',')
        else:
            raise ValueError('ERROR')

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        if type(nominal) is int and nominal > 0:
            self.__nominal = nominal
        else:
            raise ValueError('ERROR')