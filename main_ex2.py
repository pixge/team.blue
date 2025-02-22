
from src.ex2 import ex2
import math


f = 100;
fact_100 = list(range(1,f+1))

result = ex2.Multiplier.multiply(*fact_100)
print("Summable Array Result " , result.print(int))
print("math " , math.prod(fact_100) ==  result.print(int))