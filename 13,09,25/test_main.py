import unittest
from main import twoSum

class TestTwoSum(unittest.TestCase):
    def Test1(self):
        self.assertEqual(twoSum([2,7,11,15],9),[0,1])
    def Test2(self):
        self.assertEqual(twoSum([3,2,4],6),[1,2])
    def Test3(self):
        self.assertEqual(twoSum([3,3],6),[0,1])
    def EmptyTest(self):
        self.assertEqual(twoSum([],9),"Неправильные входные данные")
    def NegativeTest(self):
        self.assertEqual(twoSum([-3,7],4),[0,1])
    def NotOneTest(self):
        self.assertEqual(twoSum([0,3,6,7,2],9),[1,2])
    def NotFoundTest(self):
        self.assertEqual(twoSum([23,31],240),"Нет подходящих комбинаций")
    def NotIntTest(self):
        self.assertEqual(twoSum([5,1.32,5,7.5],5),"Неправильные входные данные")
    

if __name__ == '__main__':
    unittest.main()