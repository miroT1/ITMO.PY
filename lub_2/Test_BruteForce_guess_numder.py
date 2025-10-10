import unittest
from  main import BruteForce_guess_numder

class BruteForse(unittest.TestCase):
    def EmptyListTest(self):
        self.assertEqual(BruteForce_guess_numder(12,[]),'Incorrect input data')
    def EmptyTargetTest(self):
        self.assertEqual(BruteForce_guess_numder(None,[12,46,43,13,87]),'Incorrect input data')
    def TypeTargetTest(self):
        self.assertEqual(BruteForce_guess_numder('45',[12,46,43,6,45,6,2,1]),'Incorrect input data type')
    def TypeListtest(self):
        self.assertEqual(BruteForce_guess_numder(65,['4','23','65','89','1']),'Incorrect input data type')
    


if __name__ == '__name__':
    unittest.main()