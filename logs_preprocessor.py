import re
import pandas as pd

class LogParser:
    """
    A class to parse log files and return structured data as a Pandas DataFrame.
    """
    def __init__(self):
        # Configure Pandas to display full column content
        pd.set_option('display.max_colwidth', None)
        
        # Define the regular expression to parse logs
        self.log_pattern = re.compile(
            r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*(?P<host>[\w-]*)\s*\[(?P<level>\w+)]\s*(?P<message>.+)"
        )

    def parse(self, log_file_path):
        """
        Parses a log file into a structured Pandas DataFrame.

        Args:
            log_file_path (str): Path to the log file.

        Returns:
            pd.DataFrame: A DataFrame containing the parsed log data.
        """
        structured_logs = []
        try:
            with open(log_file_path, "r") as log_file:
                for line in log_file:
                    match = self.log_pattern.match(line.strip())
                    if match:
                        structured_logs.append(match.groupdict())
        except FileNotFoundError:
            print(f"File not found: {log_file_path}")
            return pd.DataFrame()  # Return an empty DataFrame if the file is missing

        # Convert structured logs to a Pandas DataFrame
        if structured_logs:
            return pd.DataFrame(structured_logs)
        else:
            print("No logs matched the pattern.")
            return pd.DataFrame()  # Return an empty DataFrame if no logs match
