import json
import csv


class Constants:

    class Status:
        OK = "OK"

    class Output:
        JSON = 0
        CSV = 1


class Line:
    """Line of the file loaded"""

    def __init__(self, ip: str):
        self.ip = ip
        self.bytes_sent = 0
        self.num_of_requests = 0

    def add_request(self, bytes_sent: int):
        self.bytes_sent += bytes_sent
        self.num_of_requests += 1


class Collector:
    """Main class use it, to collect dataß"""

    def __init__(self):

        self._total_bytes_sent = 0
        self._total_num_of_requests = 0
        self._lines: dict[str, Line] = dict()

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

        self._total_bytes_sent += int(bytes_sent)
        self._total_num_of_requests += 1

        line = self._lines.setdefault(remote_addr, Line(remote_addr))
        line.add_request(int(bytes_sent))

    def print(self, file_name: str, output: Constants.Output = Constants.Output.CSV):
        
        """ Print to output file
        
        Parameters:
        file_name (str): filname
        output (Constants.Output): type of the output"""

        sorted_lines = dict(
            sorted(
                self._lines.items(),
                key=lambda item: item[1].num_of_requests,
                reverse=True,
            )
        )

        if output == Constants.Output.CSV:
            return self._print_csv(file_name, sorted_lines)
        if output == Constants.Output.JSON:
            return self._print_json(file_name, sorted_lines)

    def _print_csv(self, file_name: str, sorted_lines: dict[str, Line]):

        with open(file_name, "w") as file:
            writer = csv.writer(file, delimiter=";")

            for line in sorted_lines.values():

                writer.writerow(
                    [
                        line.ip,
                        line.num_of_requests,
                        Collector._format_percent(
                            line.num_of_requests, self._total_num_of_requests
                        ),
                        line.bytes_sent,
                        Collector._format_percent(
                            line.bytes_sent, self._total_bytes_sent
                        ),
                    ]
                )

    def _print_json(self, file_name: str, sorted_lines: dict[str, Line]):

        with open(file_name, "w") as file:
            json.dump(
                {key: self._line_json_dump(line) for key, line in sorted_lines.items()},
                file,
                indent=4,
            )

    def _line_json_dump(self, line: Line):
        return {
            "ip": line.ip,
            "num_of_requests": line.num_of_requests,
            "perc_num_of_requests": Collector._format_percent(
                line.num_of_requests, self._total_num_of_requests
            ),
            "bytes_sent": line.bytes_sent,
            "perc_bytes_sent": Collector._format_percent(
                line.bytes_sent, self._total_bytes_sent
            ),
        }

    @staticmethod
    def _format_percent(a: int, b: int):
        return f"{(a / b) * 100:.2f}"
