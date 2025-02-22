from typing import Union

class SummableArray: 
    """ Class that simultate an int as an array number """
    def __init__(self, value: int):
        self.values = list(map(int, str(value)))
        self.values.reverse()
        
        
    
    def sum(self, summable : "SummableArray"):
        
        
        for i in range(len(summable.values)):
            
            self.check_and_add(i, summable.values[i])
            
           

    def check_and_add(self, i, value): 
        
        if len(self.values) <= i: 
            self.values.append(0)
            
        self.values[i] = self.values[i] + value
        
        if self.values[i] >= 10: 
            self.values[i] = self.values[i] % 10
            self.check_and_add(i+1, 1)
    

            
    def print(self, type: Union[str,int] = str) -> Union[str,int]:
        v = ''.join(map(str, self.values[::-1]))  
        return type(v)
          

class Multiplier:
    
    @staticmethod
    def _multypli_first(summables) -> SummableArray: 
       
        if len(summables) == 1:
            return summables[0]
        
        a = summables.pop(0)
        b = summables.pop(0)        
        total = SummableArray(0)
        
        for i in range(0, len(b.values)): 
            for _ in range(0, b.values[i]): 
                total.sum(a)
            a.values.insert(0, 0)
            
        summables.insert(0, total)

        return Multiplier._multypli_first(summables)
        
                         
    @staticmethod
    def multiply(*numbers) -> SummableArray:
        
        summables = [SummableArray(v) for v in numbers]
        return Multiplier._multypli_first(summables)
         
    

    
    
    
