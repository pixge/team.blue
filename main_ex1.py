
import sys
import os 
from src.ex1 import ex1

path = sys.argv[1] if len(sys.argv) > 1 else "/"
file = path + "logfiles/ipaddr.csv"

collector = ex1.Collector()
collector.load(file)

os.makedirs(path + "reports", exist_ok=True)
collector.print(path + "reports/ipaddr.csv" )
collector.print(path + "reports/ipaddr.json", ex1.Constants.Output.JSON)




