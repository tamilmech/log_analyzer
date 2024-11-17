import json


class RootCauseAnalysis:
    """
    A class to analyze root causes of system issues and provide recommendations.
    """

    def __init__(self):
        # Thresholds
        self.cpu_threshold = 80
        self.disk_threshold = 70

        # Recommendations
        self.recommendations = {
            "CPU usage": "Optimize running processes or upgrade CPU capacity.",
            "Disk usage": "Free up disk space or expand storage capacity."
        }

    def analyze(self, structured_data):
        """
        Analyze structured data for root causes and provide recommendations.

        Args:
            structured_data (list): A list of structured data dictionaries.

        Returns:
            str: A JSON string containing root causes and recommendations.
        """
        root_causes = []

        for log in structured_data:
            if log["event"] == "CPU usage" and log["value"] > self.cpu_threshold:
                root_causes.append({
                    "timestamp": log["timestamp"],
                    "root_cause": log["event"],
                    "value": log["value"],
                    "recommendation": self.recommendations["CPU usage"]
                })
            elif log["event"] == "Disk usage" and log["value"] > self.disk_threshold:
                root_causes.append({
                    "timestamp": log["timestamp"],
                    "root_cause": log["event"],
                    "value": log["value"],
                    "recommendation": self.recommendations["Disk usage"]
                })

        # Convert to JSON format
        return json.dumps({"issues": root_causes}, indent=4)
