
from src.ex1.collector import Line

import csv 
from abc import ABC, abstractmethod

class ReportSorted(ABC): 
    
    def __init__(self, lines: list[Line]):
       self._lines = lines
       self.sort()
       
       
    def sort(self): 
         self._lines = dict(
            sorted(
                self._lines.items(),
                key=lambda item: item[1].num_of_requests,
                reverse=True,
            )
        )
         
    @staticmethod
    def format_percent(a:int, b:int):
        return f"{(a / b) * 100:.2f}"

        
    @abstractmethod
    def print(self, file_path: str): 
        pass
            

    
    
    
class ReportSortedCSV(ReportSorted):
    
    def print2(self, file_path: str):
        with open(file_path, "w") as file:
            writer = csv.writer(file, delimiter=";")

            for line in self._lines.values():
                writer.writerow(
                    [
                        line.ip,
                        line.num_of_requests,
                        self.format_percent(line.num_of_requests, line.tot_num_of_requests),
                        line.bytes_sent,
                        self.format_percent(line.bytes_sent, line.tot_bytes_sent),
                    ]
                )
                

import json             
class ReportSortedJSON(ReportSorted):
    
    def print(self, file_path):
        with open(file_path, "w") as file:
            json.dump(
                {key: self._line_json_dump(line) for key, line in self._lines.items()},
                file,
                indent=4,
            )
            
    def _line_json_dump(self, line: Line):
        return {
            "ip": line.ip,
            "num_of_requests": line.num_of_requests,
            "perc_num_of_requests": self.format_percent(
                line.num_of_requests, line.tot_num_of_requests
            ),
            "bytes_sent": line.bytes_sent,
            "perc_bytes_sent": self.format_percent(
                line.bytes_sent, line.tot_bytes_sent
            ),
        }