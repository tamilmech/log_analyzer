import json

# -------------------------------------------------------------------
#                   Root Cause Analysis
# -------------------------------------------------------------------

class RootCauseAnalysis:
    """
    A class to analyze root causes of system issues and provide recommendations.
    """

    def __init__(self):
        """
        Initialize the RootCauseAnalysis class with thresholds and recommendations.

        TODO: Add support for other breaches such as 'Connection Broken', 'Instance Failed', etc.
        """
        # Thresholds for issue detection
        self.cpu_threshold: int = 80
        self.disk_threshold: int = 70

        # Recommendations for detected issues
        self.recommendations: dict[str, str] = {
            "CPU usage": "Optimize running processes or upgrade CPU capacity.",
            "Disk usage": "Free up disk space or expand storage capacity."
        }

    def analyze(self, structured_data: list[dict]) -> str:
        """
        Analyze structured data for root causes and provide recommendations.

        Args:
            structured_data (list[dict]): A list of dictionaries containing structured log data.

        Returns:
            str: A JSON string containing root causes and recommendations.

        FIXME: For recommendations, integrate GenAI lightweight LLM through API. 
               Refer to the old log analyzer implementation written by Aravind.
        """
        root_causes: list[dict] = []

        # Analyze each log for root causes
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

        # Convert issues to JSON format
        return json.dumps({"issues": root_causes}, indent=4)
