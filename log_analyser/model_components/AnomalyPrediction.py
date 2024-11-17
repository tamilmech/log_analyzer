import pandas as pd
import re
from datetime import datetime
import json


class AnomalyPrediction:
    """
    A class to extract specific metrics and failure events from log messages.
    """
    def __init__(self):
        # Define patterns for specific metrics
        self.patterns = [
            (r"CPU usage is(?: critically high:)? (\d+)%", "CPU usage"),
            (r"Disk usage is (\d+)%", "Disk usage"),
        ]
        # Define failure events to count
        self.failure_events = ["Service failures", "ETL failures"]

    def parse_message(self, message):
        """
        Extract specific metrics from a log message.

        Args:
            message (str): The log message.

        Returns:
            tuple: A tuple containing the event and its value, or (None, None) if no match is found.
        """
        for pattern, event in self.patterns:
            match = re.search(pattern, message)
            if match:
                return event, int(match.group(1))  # Convert to integer
        return None, None

    def analyze(self, df):
        """
        Analyze log messages to extract metrics and count failure events.

        Args:
            df (pd.DataFrame): DataFrame containing log messages.

        Returns:
            str: A JSON string containing structured data of anomalies.
        """
        structured_data = []

        # Extract specific metrics
        for _, row in df.iterrows():
            event, value = self.parse_message(row["message"])
            if event:
                structured_data.append({"timestamp": row["timestamp"], "event": event, "value": value})

        # Count occurrences for failure events
        for event in self.failure_events:
            count = int(df["message"].str.contains(event, case=False).sum())  # Convert to integer
            structured_data.append({"timestamp": str(datetime.now()), "event": event, "value": count})

        # Convert to JSON
        return json.dumps(structured_data, indent=4)
