
import sys
import os
from typing import Type 
from src.ex1 import collector, writer

path = sys.argv[1] if len(sys.argv) > 1 else "/"
file = path + "logfiles/ipaddr.csv"

collector =  collector.Collector()
collector.load(file)

os.makedirs(path + "reports", exist_ok=True)




def print_report(file_path: str, clazz: Type[writer.ReportSorted]):
    report = clazz(collector.lines)
    report.print(file_path)

print_report(path + "reports/ipaddr.csv", writer.ReportSortedCSV)
print_report(path + "reports/ipaddr.json", writer.ReportSortedJSON)


# collector.print(path + "reports/ipaddr.csv" )
# collector.print(path + "reports/ipaddr.json", ex1.Constants.Output.JSON)




