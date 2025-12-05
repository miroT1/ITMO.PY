from models.author import Author

class App:
    def __init__(self, name: str, version: str, author: Author):
        self.__name: str = None
        self.__version: str = None
        self.__author: Author = None
        self.name = name
        self.version = version
        self.author = author

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
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        if type(version) is str and len(version.split('.')) >= 1:
            self.__version = version
        else:
            raise ValueError('ERROR')

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author: Author):
        if isinstance(author, Author):
            self.__author = author
        else:
            raise TypeError('ERROR')