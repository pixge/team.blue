import unittest
import math 

from src.ex2 import ex2

class TestEx2(unittest.TestCase): 
            
    def setUp(self):
        # print(f"\nRunning test: {self._testMethodName}")
        pass
        
    def compare(self, values: list[int]):
        summable_array = ex2.Multiplier.multiply(*values)
        self.assertEqual(math.prod(values), summable_array.print(int))
        # print(math.prod(values), summable_array.values)
                    
    def test_1_x_1(self): 
        self.compare([1,1])   
             
    def test_1(self): 
        self.compare([61])        
        
    def test_factor_100(self):
        self.compare(list(range(1,101)))
       
    def recursive_loop(self, index, values = [], max_range=15): 
        index = index -1
        for i in range(1,max_range): 
            new_values = values.copy();
            new_values.append(i)
            if index == 0:
                self.compare(new_values)
            else: 
                self.recursive_loop(index, new_values)
                 
    def test_arguments(self):
        self.recursive_loop(2)
        self.recursive_loop(3)
        self.recursive_loop(4)
   
    def test_9999(self):
       self.compare([9999, 5])
    
        