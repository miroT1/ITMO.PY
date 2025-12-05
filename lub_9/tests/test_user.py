import unittest
from models.user import User


class TestUserModel(unittest.TestCase):
    def test_user_creation(self) -> None:
        user = User("Иван Иванов")
        self.assertEqual(user.name, "Иван Иванов")

    def test_user_name_setter_valid(self) -> None:
        user = User("Иван Иванов")
        user.name = "Петр Петров"
        self.assertEqual(user.name, "Петр Петров")

    def test_user_name_setter_invalid_empty(self) -> None:
        user = User("Иван Иванов")
        with self.assertRaises(ValueError) as context:
            user.name = ""
        self.assertEqual(str(context.exception), "Имя пользователя не может быть пустым")

    def test_user_name_setter_invalid_whitespace(self) -> None:
        user = User("Иван Иванов")

        with self.assertRaises(ValueError) as context:
            user.name = "   "

        self.assertEqual(str(context.exception), "Имя пользователя не может быть пустым")
    def test_user_name_trimming(self) -> None:
        user = User("  Иван Иванов  ")
        self.assertEqual(user.name, "Иван Иванов")


if __name__ == "__main__":
    unittest.main()
