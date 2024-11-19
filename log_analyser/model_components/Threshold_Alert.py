import json
import os
import sys

# -------------------------------------------------------------------
#                   Threshold Alert
# -------------------------------------------------------------------

# Add the parent directory to sys.path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the required configuration
from config.paths import MainPath


class ThresholdAlert:
    """
    A class to analyze structured data against thresholds and provide alerts with recommendations.
    """

    def __init__(self):
        """
        Initialize the ThresholdAlert class with thresholds and recommendations.

        TODO: Threshold values should be dynamically adjustable via a UI input.
        FIXME: Current thresholds are static; ensure real-time updates to thresholds in future implementations.
        """
        # Initialize thresholds from MainPath 
        self.cpu_threshold: int = MainPath.cpu_threshold
        self.disk_threshold: int = MainPath.disk_threshold
        self.critical_threshold: int = MainPath.critical_threshold

        # Recommendations for root causes
        self.recommendations: dict[str, str] = {
            "CPU usage": "Optimize running processes or upgrade CPU capacity.",
            "Disk usage": "Free up disk space or expand storage capacity."
        }

    def analyze(self, structured_data: list[dict]) -> str:
        """
        Analyze structured data for threshold violations and provide recommendations.

        Args:
            structured_data (list[dict]): A list of dictionaries containing structured log data.

        Returns:
            str: A JSON string containing threshold alerts and recommendations.

        FIXME: Extend support for more complex recommendation logic, potentially using AI or historical log analysis.
        """
        root_causes: list[dict] = []

        # Analyze each log for threshold violations
        for log in structured_data:
            # Check for CPU threshold violations
            if log["event"] == "CPU usage" and log["value"] > self.cpu_threshold:
                root_causes.append({
                    "timestamp": log["timestamp"],
                    "root_cause": log["event"],
                    "value": log["value"],
                    "recommendation": self.recommendations["CPU usage"]
                })
            # Check for Disk threshold violations
            elif log["event"] == "Disk usage" and log["value"] > self.disk_threshold:
                root_causes.append({
                    "timestamp": log["timestamp"],
                    "root_cause": log["event"],
                    "value": log["value"],
                    "recommendation": self.recommendations["Disk usage"]
                })
            # Check for Critical threshold violations
            if log["value"] > self.critical_threshold:
                root_causes.append({
                    "timestamp": log["timestamp"],
                    "root_cause": f"Critical {log['event']}",
                    "value": log["value"],
                    "recommendation": f"Immediate attention required: {self.recommendations.get(log['event'], 'Check system health.')}"
                })

        # Convert results to JSON format
        return json.dumps({"issues": root_causes}, indent=4)


# -------------------------------------------------------------------
#                   Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":
    """
    Main block for testing the ThresholdAlert class with example data.
    """
    # Example structured data
    example_data = [
        {"timestamp": "2024-11-18T10:00:00", "event": "CPU usage", "value": 85},
        {"timestamp": "2024-11-18T11:00:00", "event": "Disk usage", "value": 72},
        {"timestamp": "2024-11-18T12:00:00", "event": "CPU usage", "value": 95},
        {"timestamp": "2024-11-18T13:00:00", "event": "Disk usage", "value": 91}
    ]

    # Initialize ThresholdAlert and analyze example data
    threshold_alert = ThresholdAlert()
    results = threshold_alert.analyze(example_data)

    # Print the analysis results
    print(results)
