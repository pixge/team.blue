import unittest
import os 
from src.ex1 import collector, writer

class TestEx1(unittest.TestCase): 
            
    def setUp(self):
        self.collector = collector.Collector() 
        self.outfile = "test.output"
    
    def tearDown(self):
        os.remove(self.outfile)
        # pass
        
    def print_and_parse(self, collector: collector.Collector):
        report = writer.ReportSortedCSV(collector.lines)
        report.print(self.outfile)
        return self.csv_to_dict()
                
    def test_one_line(self): 
        self.collector.add(TestEx1.create_line("1", 10))
        
        data = self.print_and_parse(self.collector)
        self.assert_ip_equals(data.get("1"), 1, 100, 10, 100)
   
    def test_two_line(self): 
        self.collector.add(TestEx1.create_line("1", 10))
        self.collector.add(TestEx1.create_line("1", 60))
       
        data = self.print_and_parse(self.collector)
        self.assert_ip_equals(data.get("1"), 2, 100, 70, 100)
   
    def test_exclude_stat_line(self): 
        self.collector.add(TestEx1.create_line("1", 10))
        self.collector.add(TestEx1.create_line("1", 10, False))

        data = self.print_and_parse(self.collector)
        self.assert_ip_equals(data.get("1"), 1, 100, 10, 100)
   
    def test_perc_stat_line(self): 
        self.collector.add(TestEx1.create_line("1", 0))
        self.collector.add(TestEx1.create_line("1", 0))
        self.collector.add(TestEx1.create_line("1", 0))
        self.collector.add(TestEx1.create_line("1", 0))
        self.collector.add(TestEx1.create_line("2", 50))
        self.collector.add(TestEx1.create_line("3", 0))
        self.collector.add(TestEx1.create_line("4", 25))
        self.collector.add(TestEx1.create_line("4", 25))
        
        data = self.print_and_parse(self.collector)
        self.assert_ip_equals(data.get("1"), 4, 50, 0, 0)
        self.assert_ip_equals(data.get("2"), 1, 12.5, 50, 50)
        self.assert_ip_equals(data.get("3"), 1, 12.5, 0, 0)
        self.assert_ip_equals(data.get("4"), 2, 25, 50, 50)
        
        
    def test_order(self): 
        self.collector.add(TestEx1.create_line("1", 0))
        self.collector.add(TestEx1.create_line("1", 0))
        self.collector.add(TestEx1.create_line("1", 0))
        self.collector.add(TestEx1.create_line("1", 0))
        self.collector.add(TestEx1.create_line("2", 50))
        self.collector.add(TestEx1.create_line("2", 50))
        self.collector.add(TestEx1.create_line("2", 50))
        self.collector.add(TestEx1.create_line("2", 50))
        self.collector.add(TestEx1.create_line("2", 50))
        self.collector.add(TestEx1.create_line("2", 50))
        self.collector.add(TestEx1.create_line("3", 0))
        self.collector.add(TestEx1.create_line("3", 0))
        self.collector.add(TestEx1.create_line("4", 25))
        self.collector.add(TestEx1.create_line("4", 25))
        self.collector.add(TestEx1.create_line("4", 25))
        self.collector.add(TestEx1.create_line("4", 25))

        data = self.print_and_parse(self.collector)
        
        max_num_of_request = None
        for ip in data.values(): 
            num_of_requests = ip.get("num_of_requests")
            self.assertLessEqual(num_of_requests, max_num_of_request if max_num_of_request is not None else num_of_requests)
            max_num_of_request = num_of_requests

   
    
    def assert_ip_equals(self, ip, num_of_requests, perc_num_of_requests, bytes_sent, perc_bytes_sent): 
        self.assertEqual(int(ip.get("num_of_requests")), num_of_requests)
        self.assertEqual(ip.get("perc_num_of_requests"), f"{perc_num_of_requests:.2f}" )
        self.assertEqual(int(ip.get("bytes_sent")), bytes_sent)
        self.assertEqual(ip.get("perc_bytes_sent"), f"{perc_bytes_sent:.2f}")
        


    def csv_to_dict(self): 
        data = dict()
        with open(self.outfile, "r") as stream:
            for line in stream: 
                ip, num_of_requests, perc_num_of_requests, bytes_sent, perc_bytes_sent = line.strip().split(";")
                data.setdefault(ip, {
                    "num_of_requests": num_of_requests,
                    "perc_num_of_requests": perc_num_of_requests,
                    "bytes_sent": bytes_sent,
                    "perc_bytes_sent":perc_bytes_sent
                })
                
            
        return data                
        
    @staticmethod
    def create_line(ip, bytes, status = True):
        return "1234; "+ str(bytes) +";"+ ("200" if status else "500")  +";"+ ip
        