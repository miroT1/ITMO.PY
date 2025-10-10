import unittest
from main import bruteforce_guess_number
from main import binary_guess_number

class bruteforse(unittest.TestCase):
    def EmptyListTest(self):
        self.assertEqual(bruteforce_guess_number(12, []),None, 'Incorrect input data')
    def TypeTargetTest(self):
        self.assertEqual(bruteforce_guess_number(34567890, [12, 46, 43, 6, 45, 6, 2, 1]), 'Incorrect input data type')
    def TypeListtest(self):
        self.assertEqual(bruteforce_guess_number(65, ['4', '23', '65', '89', '1']), 'Incorrect input data type')
    def test(self):
        self.assertEqual(bruteforce_guess_number(12, [12,34,45,56,67,87]),[12,1], 'Incorrect input data')

class binary(unittest.TestCase):
    def EmptyListTest(self):
        self.assertEqual(binary_guess_number(12, []), 'Incorrect input data')
    def TypeTargetTest(self):
        self.assertEqual(bruteforce_guess_number(34567890, [12, 46, 43, 6, 45, 6, 2, 1]), 'Incorrect input data type')
    def TypeListtest(self):
        self.assertEqual(bruteforce_guess_number(65, ['4', '23', '65', '89', '1']), 'Incorrect input data type')
    def test(self):
        self.assertEqual(bruteforce_guess_number(12, [12,34,45,56,67,87]),[12,1], 'Incorrect input data')

if __name__ == '__name__':
    unittest.main()