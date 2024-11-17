import json


class ThresholdAlert:
    """
    A class to analyze structured data against thresholds and provide alerts with recommendations.
    """

    def __init__(self):
        # Thresholds
        self.cpu_threshold = 80
        self.disk_threshold = 70
        self.critical_threshold = 90

        # Recommendations
        self.recommendations = {
            "CPU usage": "Optimize running processes or upgrade CPU capacity.",
            "Disk usage": "Free up disk space or expand storage capacity."
        }

    def analyze(self, structured_data):
        """
        Analyze structured data for threshold violations and provide recommendations.

        Args:
            structured_data (list): A list of structured data dictionaries.

        Returns:
            str: A JSON string containing threshold alerts and recommendations.
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
            # Check for critical threshold violations
            if log["value"] > self.critical_threshold:
                root_causes.append({
                    "timestamp": log["timestamp"],
                    "root_cause": f"Critical {log['event']}",
                    "value": log["value"],
                    "recommendation": f"Immediate attention required: {self.recommendations.get(log['event'], 'Check system health.')}"
                })

        # Convert to JSON format
        return json.dumps({"issues": root_causes}, indent=4)
