class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_id: str):
        self.__id: int = None
        self.__user_id: int = None
        self.__currency_id: str = None

        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if type(id) is int and id > 0:
            self.__id = id
        else:
            raise ValueError('ERROR')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        if type(user_id) is int and user_id > 0:
            self.__user_id = user_id
        else:
            raise ValueError('ERROR')

    @property
    def currency_id(self):
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: str):
        if type(currency_id) is str and len(currency_id) > 0:
            self.__currency_id = currency_id
        else:
            raise ValueError('ERROR')