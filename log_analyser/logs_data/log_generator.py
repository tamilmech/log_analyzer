import random
import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to sys.path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the required configuration
from config.paths import MainPath

# -------------------------------------------------------------------
#                   Log Generator
# -------------------------------------------------------------------

class LogGenerator:
    """
    A class to generate synthetic logs for testing purposes.
    """

    def __init__(self):
        """
        Initialize the LogGenerator with predefined services, topics, and templates.
        """
        # Define dynamic placeholders for different logs
        self.SERVICES = ["Kafka", "Airflow", "Python", "Java", "AWS", "Azure", "Docker", "Kubernetes"]
        self.TOPICS = ["topic_orders", "topic_users", "topic_transactions", "topic_events"]
        self.HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        self.HTTP_URLS = [
            "/api/v1/users",
            "/api/v1/orders",
            "/api/v2/transactions",
            "/admin/dashboard",
            "/healthcheck",
        ]
        self.TASKS = ["task_etl", "task_data_validation", "task_api_sync", "task_model_training"]
        self.DAGS = ["dag_sales_pipeline", "dag_user_sync", "dag_data_ingestion", "dag_model_training"]
        self.EMAILS = ["john.doe@example.com", "alice.smith@test.com", "user123@domain.org"]
        self.PHONE_NUMBERS = ["9876543210", "9123456789", "9988776655"]

        # Positive log templates
        self.POSITIVE_TEMPLATES = [
            "{timestamp} [INFO] {service} operation completed successfully. Processed 1500 records in 2.35 seconds.",
            "{timestamp} [INFO] CPU usage is {cpu_usage}%. Threshold not exceeded. System operating normally.",
            "{timestamp} [INFO] Disk usage is {disk_usage}%. Disk space within acceptable limits.",
            "{timestamp} [INFO] Published message to topic '{topic}' using {service}. Message delivery confirmed after 10 retries.",
            "{timestamp} [INFO] {method} request to {url} succeeded. Response code: 200 OK. Response size: 1.2MB.",
            "{timestamp} [INFO] Task '{task}' in DAG '{dag}' completed successfully in 45 seconds.",
            "{timestamp} [INFO] User {email} logged in from IP 192.168.0.{ip_suffix}. Login duration: 10 minutes.",
            "{timestamp} [INFO] Phone number {phone} was successfully added to the system.",
            "{timestamp} [INFO] Docker container started successfully for service {service}. Container ID: abcd1234efgh5678.",
            "{timestamp} [INFO] Kubernetes pod scaled up successfully. New replicas: 5.",
            "{timestamp} [INFO] Lambda function executed successfully in AWS. Execution duration: 250ms.",
        ]

        # Negative log templates
        self.NEGATIVE_TEMPLATES = [
            "{timestamp} [ERROR] {service} encountered an issue. Exception: NullPointerException in thread 'main'.",
            "{timestamp} [ERROR] CPU usage is critically high: {cpu_usage}%. Immediate action required.",
            "{timestamp} [ERROR] Disk usage is critically high: {disk_usage}%. Threshold exceeded on volume /dev/sda1.",
            "{timestamp} [ERROR] Failed to consume message from topic '{topic}' using {service}. Error: TimeoutException after 30 seconds.",
            "{timestamp} [ERROR] {method} request to {url} failed. Response code: 500 Internal Server Error. Error details: Missing authentication token.",
            "{timestamp} [ERROR] Task '{task}' in DAG '{dag}' failed after 3 retries. Error: Data validation error in step 2.",
            "{timestamp} [ERROR] Phone number {phone} could not be added due to a duplicate record conflict in the database.",
            "{timestamp} [ERROR] Docker container failed to start for service {service}. Error log: Container crashed on startup.",
            "{timestamp} [ERROR] Kubernetes pod crash detected. Pod ID: kube_pod12345.",
            "{timestamp} [ERROR] Lambda function execution failed in AWS. Error: Invalid parameters provided.",
        ]

    def generate_log(self, template: str, timestamp: datetime) -> str:
        """
        Generate a single log entry based on a template.

        Args:
            template (str): The log template to format.
            timestamp (datetime): The timestamp for the log.

        Returns:
            str: A formatted log entry.
        """
        return template.format(
            timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            service=random.choice(self.SERVICES),
            method=random.choice(self.HTTP_METHODS),
            url=random.choice(self.HTTP_URLS),
            topic=random.choice(self.TOPICS),
            task=random.choice(self.TASKS),
            dag=random.choice(self.DAGS),
            email=random.choice(self.EMAILS),
            phone=random.choice(self.PHONE_NUMBERS),
            cpu_usage=random.randint(10, 90),  # CPU usage percentage
            disk_usage=random.randint(10, 95),  # Disk usage percentage
            ip_suffix=random.randint(1, 255),  # Random IP suffix
        )

    def generate_hourly_logs(self, start_time: datetime, num_hours: int, logs_per_hour: int, output_file: str = None) -> list[str]:
        """
        Generate logs for a specified number of hours and save to a file.

        Args:
            start_time (datetime): The starting timestamp for log generation.
            num_hours (int): Number of hours to generate logs for.
            logs_per_hour (int): Number of logs to generate per hour.
            output_file (str, optional): Path to save the generated logs. Defaults to None.

        Returns:
            list[str]: A list of generated log entries.
        """
        logs = []
        current_time = start_time

        for _ in range(num_hours):
            for _ in range(logs_per_hour):
                # Randomly choose a positive or negative template
                template = random.choice(
                    self.NEGATIVE_TEMPLATES if random.random() < 0.4 else self.POSITIVE_TEMPLATES
                )
                try:
                    log_entry = self.generate_log(template, current_time)
                    logs.append(log_entry)
                except KeyError as e:
                    print(f"Template formatting error: {e}")
                    continue

                # Increment time by a random interval (1–10 minutes)
                current_time += timedelta(minutes=random.randint(1, 10))
            # Move to the next hour
            current_time = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

        # Write logs to a file
        if output_file:
            with open(output_file, "w") as file:
                file.write("\n".join(logs))

        return logs


# -------------------------------------------------------------------
#                   Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":
    """
    Main block for testing the LogGenerator class.
    """
    start_time = datetime.now().replace(minute=0, second=0, microsecond=0)  # Start from the current hour
    num_hours = 15  # Number of hours to generate logs for
    logs_per_hour = 20  # Number of logs per hour
    output_file_path = f"{MainPath.folder_path}/log_analyser/logs_data/data_logs.txt"  # File to save logs

    # Initialize LogGenerator and generate logs
    log_generator = LogGenerator()
    logs = log_generator.generate_hourly_logs(start_time, num_hours, logs_per_hour, output_file_path)
    print(f"\nGenerated logs saved to {output_file_path}")
