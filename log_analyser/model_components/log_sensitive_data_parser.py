import re
import json
import pandas as pd

# -------------------------------------------------------------------
#                   Sensitive Data Parser
# -------------------------------------------------------------------

class SensitiveDataParser:
    """
    A class to parse sensitive data from log messages.
    """

    def __init__(self):
        """
        Initialize the SensitiveDataParser with predefined patterns for various types of sensitive data.

        TODO: Add advanced parsing capabilities using SpaCy for improved accuracy and context understanding.
        """
        
        # HACK: Temporarily using this method until we find a better solution
        
        # Define patterns for sensitive data
        self.patterns: dict[str, str] = {
            "email": r"[\w\.-]+@[\w\.-]+\.com",
            "credit_card": r"\b(?:\d{4}-){3}\d{4}\b",
            "api_key": r"\b[A-Z0-9]{16,}\b",
            "phone": r"\b\d{10}\b",
            "token": r"\b[A-Z0-9]{16,}\b",
            "password": r"Password '([^']+)'"
        }

    def parse(self, df: pd.DataFrame) -> list[dict]:
        """
        Parses sensitive data from the given DataFrame.

        Args:
            df (pd.DataFrame): A DataFrame containing a 'message' column.

        Returns:
            list[dict]: A list of dictionaries containing parsed sensitive data entries.

        Raises:
            ValueError: If the DataFrame does not contain the required 'message' column.

        FIXME: Ensure better timestamp parsing for logs that do not follow a standard timestamp format.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        parsed_data: list[dict] = []

        # Parse each log message for sensitive data
        for log in df['message']:
            timestamp = log.split(" [")[0]  # Extract timestamp (assumes specific log format)
            for data_type, pattern in self.patterns.items():
                match = re.search(pattern, log)
                if match:
                    # Extract the detected value (handle special cases like password separately)
                    detected_value = match.group(1) if data_type == "password" else match.group(0)
                    parsed_data.append({
                        "timestamp": timestamp,
                        "sensitive_data_type": data_type,
                        "detected_value": detected_value,
                        "log_message": log
                    })

        return parsed_data
