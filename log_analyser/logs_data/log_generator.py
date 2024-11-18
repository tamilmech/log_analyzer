import random
from datetime import datetime, timedelta

# Define dynamic placeholders for different logs
SERVICES = ["Kafka", "Airflow", "Python", "Java", "AWS", "Azure", "Docker", "Kubernetes"]
TOPICS = ["topic_orders", "topic_users", "topic_transactions", "topic_events"]
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
HTTP_URLS = [
    "/api/v1/users",
    "/api/v1/orders",
    "/api/v2/transactions",
    "/admin/dashboard",
    "/healthcheck",
]
TASKS = ["task_etl", "task_data_validation", "task_api_sync", "task_model_training"]
DAGS = ["dag_sales_pipeline", "dag_user_sync", "dag_data_ingestion", "dag_model_training"]

EMAILS = ["john.doe@example.com", "alice.smith@test.com", "user123@domain.org"]
PHONE_NUMBERS = ["9876543210", "9123456789", "9988776655"]

# Positive log templates
POSITIVE_TEMPLATES = [
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
NEGATIVE_TEMPLATES = [
    "{timestamp} [ERROR] {service} encountered an issue. Exception: NullPointerException in thread 'main'.",
    "{timestamp} [ERROR] CPU usage is critically high: {cpu_usage}%. Immediate action required.",
    "{timestamp} [ERROR] Disk usage is critically high: {disk_usage}%. Threshold exceeded on volume /dev/sda1.",
    "{timestamp} [ERROR] Failed to consume message from topic '{topic}' using {service}. Error: TimeoutException after 30 seconds.",
    "{timestamp} [ERROR] {method} request to {url} failed. Response code: 500 Internal Server Error. Error details: Missing authentication token.",
    "{timestamp} [ERROR] Task '{task}' in DAG '{dag}' failed after 3 retries. Error: Data validation error in step 2.",
    "{timestamp} [ERROR] Task '{task}' in DAG '{dag}' failed after 3 retries. Error: Service failures .",
    "{timestamp} [ERROR] Phone number {phone} could not be added due to a duplicate record conflict in the database.",
    "{timestamp} [ERROR] Docker container failed to start for service {service}. Error log: Container crashed on startup.",
    "{timestamp} [ERROR] Kubernetes pod crash detected. Pod ID: kube_pod12345.",
    "{timestamp} [ERROR] Oreder pipeline container ETL failures . Pod ID: kube_pod12345.",
    "{timestamp} [ERROR] Lambda function execution failed in AWS. Error: Invalid parameters provided.",
]

# Generate a single log for a given template
def generate_log(template, timestamp):
    return template.format(
        timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        service=random.choice(SERVICES),
        method=random.choice(HTTP_METHODS),
        url=random.choice(HTTP_URLS),
        topic=random.choice(TOPICS),
        task=random.choice(TASKS),
        dag=random.choice(DAGS),
        email=random.choice(EMAILS),
        phone=random.choice(PHONE_NUMBERS),
        cpu_usage=random.randint(10, 90),  # CPU usage percentage
        disk_usage=random.randint(10, 95),  # Disk usage percentage
        ip_suffix=random.randint(1, 255),  # Random IP suffix
    )

# Generate logs for each hour
def generate_hourly_logs(start_time, num_hours, logs_per_hour, output_file=None):
    logs = []
    current_time = start_time

    for _ in range(num_hours):
        for _ in range(logs_per_hour):
            # Randomly choose a positive or negative template
            if random.random() < 0.4:  # 40% chance for a negative log
                template = random.choice(NEGATIVE_TEMPLATES)
            else:  # 60% chance for a positive log
                template = random.choice(POSITIVE_TEMPLATES)

            try:
                log_entry = generate_log(template, current_time)
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

    # Return logs for optional use
    return logs

# Main function
if __name__ == "__main__":
    start_time = datetime.now().replace(minute=0, second=0, microsecond=0)  # Start from the current hour
    num_hours = 30  # Number of hours to generate logs for
    logs_per_hour = 40  # Number of logs per hour
    output_file_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/logs_data/data_logs.txt"  # File to save logs
    logs = generate_hourly_logs(start_time, num_hours, logs_per_hour, output_file_path)
    print(f"\nGenerated logs with separate CPU and Disk usage saved to {output_file_path}")
