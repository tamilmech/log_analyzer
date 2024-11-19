# -------------------------------------------------------------------
#                   Main Path Configuration & Threshold Alert settings
# -------------------------------------------------------------------

from dataclasses import dataclass

@dataclass
class MainPath:
    """
    Represents the main path configuration for the log analyzer.
    """

    folder_path: str = "/Users/tamilselavans/Desktop/log_analyzer/"  # Main folder for log analyzer data and outputs
    cpu_threshold: int = 90  # CPU usage threshold in percentage
    disk_threshold: int = 90  # Disk usage threshold in percentage
    critical_threshold: int = 90  # Critical system threshold in percentage
