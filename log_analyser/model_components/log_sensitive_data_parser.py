import re
import json

class SensitiveDataParser:
    """
    A class to parse sensitive data from logs.
    """
    def __init__(self):
        # Define patterns for sensitive data
        self.patterns = {
            "email": r"[\w\.-]+@[\w\.-]+\.com",
            "credit_card": r"\b(?:\d{4}-){3}\d{4}\b",
            "api_key": r"\b[A-Z0-9]{16,}\b",
            "phone": r"\b\d{10}\b",
            "token": r"\b[A-Z0-9]{16,}\b",
            "password": r"Password '([^']+)'"
        }

    def parse(self, df):
        """
        Parses sensitive data from the given DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing a 'message' column.

        Returns:
            list: A list of parsed sensitive data entries.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        parsed_data = []

        # Parse each log message
        for log in df['message']:
            timestamp = log.split(" [")[0]  # Extract timestamp
            for data_type, pattern in self.patterns.items():
                match = re.search(pattern, log)
                if match:
                    detected_value = match.group(1) if data_type == "password" else match.group(0)
                    parsed_data.append({
                        "timestamp": timestamp,
                        "sensitive_data_type": data_type,
                        "detected_value": detected_value,
                        "log_message": log
                    })

        return parsed_data
