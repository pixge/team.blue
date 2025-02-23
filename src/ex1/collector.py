

class Constants:

    class Status:
        OK = "OK"

class Total: 
    def __init__(self):
        self._total_num_of_requests = 0
        self._total_bytes_sent = 0

class Line:
    """Line of the file loaded"""

    def __init__(self, ip: str, total: Total):
        self.ip = ip
        self.bytes_sent = 0
        self.num_of_requests = 0
        self._total = total

    def add_request(self, bytes_sent: int):
        self.bytes_sent += bytes_sent
        self.num_of_requests += 1
        
    @property
    def tot_num_of_requests(self):
        return self._total._total_num_of_requests
    
    @property
    def tot_bytes_sent(self):
        return self._total._total_bytes_sent


class Collector:
    """Main class use it, to collect dataß"""
            
    def __init__(self):

        self._lines: dict[str, Line] = dict()
        self._total = Total()

    def load(self, file: str):
        """Load the file containing the lines
        Parameters:
        file (str): file path
        """
        with open(file, "r") as stream:
            for line in stream:
                self.add(line)

    def add(self, line: str):

        _, bytes_sent, status, remote_addr = line.strip().split(";")

        if status != Constants.Status.OK:
            return

        self._total._total_bytes_sent += int(bytes_sent)
        self._total._total_num_of_requests += 1

        line = self._lines.setdefault(remote_addr, Line(remote_addr, self._total))
        line.add_request(int(bytes_sent))


    @property
    def lines(self):
        return self._lines