import pandas as pd
import re
from datetime import datetime
import json

# -------------------------------------------------------------------
#                   Anomaly Prediction
# -------------------------------------------------------------------

class AnomalyPrediction:
    """
    A class to extract specific metrics and count failure events from log messages.
    """

    def __init__(self):
        """
        Initialize the AnomalyPrediction class with patterns for specific metrics 
        and a list of failure events to monitor.
        """
        # Define patterns for specific metrics
        self.patterns: list[tuple[str, str]] = [
            (r"CPU usage is(?: critically high:)? (\d+)%", "CPU usage"),
            (r"Disk usage is (\d+)%", "Disk usage"),
        ]
        # Define failure events to count
        self.failure_events: list[str] = ["Service failures", "ETL failures"]

    def parse_message(self, message: str) -> tuple[str | None, int | None]:
        """
        Extract specific metrics from a log message using predefined patterns.

        Args:
            message (str): The log message.

        Returns:
            tuple[str | None, int | None]: A tuple containing the event name and its value, 
                                           or (None, None) if no match is found.
        """
        for pattern, event in self.patterns:
            match = re.search(pattern, message)
            if match:
                return event, int(match.group(1))  # Convert the extracted value to an integer
        return None, None

    def analyze(self, df: pd.DataFrame) -> str:
        """
        Analyze log messages to extract specific metrics and count failure events.

        Args:
            df (pd.DataFrame): DataFrame containing log messages.

        Returns:
            str: A JSON string containing structured data of anomalies.
        """
        structured_data: list[dict] = []

        # Extract specific metrics from log messages
        for _, row in df.iterrows():
            event, value = self.parse_message(row["message"])
            if event:
                structured_data.append({
                    "timestamp": str(row["timestamp"]),  # Convert to string for JSON serialization
                    "event": event,
                    "value": value
                })

        # Count occurrences of predefined failure events
        for event in self.failure_events:
            count: int = int(df["message"].str.contains(event, case=False).sum())
            structured_data.append({
                "timestamp": str(datetime.now()),  # Current timestamp as a string
                "event": event,
                "value": count
            })

        # Return the structured data as a JSON string
        return json.dumps(structured_data, indent=4)
