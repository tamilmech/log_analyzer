import logging
import os
import json
from contextlib import redirect_stdout

from logs_preprocessor import LogParser
from model_components.SentimentAnalysis import SentimentAnalysis
from model_components.log_sensitive_data_parser import SensitiveDataParser
from model_components.clustering_keywords import KeywordClustering
from model_components.AnomalyPrediction import AnomalyPrediction
from model_components.Root_Cause_Analysis import RootCauseAnalysis
from model_components.Threshold_Alert import ThresholdAlert
from model_components.DBSCAN_Clustering import DBSCANClustering
from model_components.HDBSCAN_Clustering import HDBSCANClustering

# Configure logging
logging.basicConfig(
    filename="log_analyzer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def save_output(df, output_path, filename):
    """
    Save DataFrame to CSV and JSON output to the given path.
    """
    # Save DataFrame to CSV
    csv_path = os.path.join(output_path, f"{filename}.csv")
    df.to_csv(csv_path, index=False)
    logging.info(f"Saved CSV output: {csv_path}")

    # Save DataFrame to JSON
    json_path = os.path.join(output_path, f"{filename}.json")
    df.to_json(json_path, orient="records", lines=True)
    logging.info(f"Saved JSON output: {json_path}")

def save_json_output(data, output_path, filename):
    """
    Save JSON output to the given path, ensuring proper formatting.
    """
    # If data is a JSON string, parse it to a Python dictionary
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON string: {e}")
            return

    # Save the JSON object with proper formatting
    json_path = os.path.join(output_path, f"{filename}.json")
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    logging.info(f"Saved JSON output: {json_path}")

def main():
    logging.info("Starting log analysis")

    # Define the path to the sample log file
    log_file_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/logs_data/data_logs.txt"  # Replace with the actual path to your log file
    logging.info(f"Log file path: {log_file_path}")

    # Output path for results
    output_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/model_outputs"
    os.makedirs(output_path, exist_ok=True)

    # Initialize the LogParser
    logging.info("Initializing LogParser")
    log_parser = LogParser()

    # Parse the log file
    logging.info("Parsing the log file")
    df = log_parser.parse(log_file_path)
    if df.empty:
        logging.warning("No valid logs to display.")
        print("No valid logs to display.")
        return
    logging.info("Parsed logs successfully")
    print(df[['level', 'message']])

    # Save the parsed logs to CSV and JSON
    save_output(df, output_path, "parsed_logs")

    # Initialize the SentimentAnalysis class
    logging.info("Initializing SentimentAnalysis")
    sentiment_analyzer = SentimentAnalysis()

    # Analyze the sentiment of the messages
    logging.info("Analyzing sentiment of log messages")
    analyzed_df = sentiment_analyzer.analyze(df)
    logging.info("Sentiment analysis completed")
    print("Analyzed Logs:")
    print(analyzed_df[['message', 'Sentiment']])

    # Save sentiment analysis results to CSV and JSON
    save_output(analyzed_df, output_path, "sentiment_analysis_results")

    # Initialize the SensitiveDataParser
    logging.info("Initializing SensitiveDataParser")
    sensitive_data_parser = SensitiveDataParser()

    # Parse sensitive data
    logging.info("Parsing sensitive data")
    sensitive_data = sensitive_data_parser.parse(df)
    logging.info("Sensitive data parsing completed")
    print("Parsed Sensitive Data:")
    print(json.dumps(sensitive_data, indent=4))

    # Save sensitive data to JSON
    save_json_output(sensitive_data, output_path, "sensitive_data")

    # Initialize the KeywordClustering class
    logging.info("Initializing KeywordClustering")
    keyword_clustering = KeywordClustering()

    # Categorize the messages into clusters
    logging.info("Clustering messages into categories")
    clustered_df = keyword_clustering.categorize(df)
    logging.info("Keyword clustering completed")
    print("Clustered Logs:")
    print(clustered_df[['message', 'Keyword_cluster']])

    # Save clustering results to CSV and JSON
    save_output(clustered_df, output_path, "keyword_clustering_results")

    # Initialize the AnomalyPrediction class
    logging.info("Initializing AnomalyPrediction")
    anomaly_predictor = AnomalyPrediction()

    # Extract specific metrics and failure events
    logging.info("Extracting anomalies from log messages")
    anomalies_json = anomaly_predictor.analyze(df)
    logging.info("Anomaly prediction completed")

    # Deserialize anomalies JSON
    try:
        structured_data = json.loads(anomalies_json) if isinstance(anomalies_json, str) else anomalies_json
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode anomalies JSON: {e}")
        print("Failed to decode anomalies JSON")
        return

    # Pretty print the deserialized anomalies
    logging.info("Structured anomalies data successfully parsed")
    print("Extracted Anomalies:")
    print(json.dumps(structured_data, indent=4))

    # Save anomalies JSON to file
    save_json_output(structured_data, output_path, "anomalies")

    # Initialize the RootCauseAnalysis class
    logging.info("Initializing RootCauseAnalysis")
    root_cause_analyzer = RootCauseAnalysis()

    # Analyze the root causes and provide recommendations
    logging.info("Analyzing root causes")
    root_cause_json = root_cause_analyzer.analyze(structured_data)
    logging.info("Root cause analysis completed")
    print("Root Causes and Recommendations:")
    print(json.dumps(root_cause_json, indent=4))

    # Save root cause analysis results to JSON
    save_json_output(root_cause_json, output_path, "root_cause_analysis")

    # Initialize the ThresholdAlert class
    logging.info("Initializing ThresholdAlert")
    threshold_alert = ThresholdAlert()

    # Analyze the thresholds and provide alerts
    logging.info("Analyzing thresholds for alerts")
    threshold_alert_json = threshold_alert.analyze(structured_data)
    logging.info("Threshold alert analysis completed")

    # Pretty print the threshold alerts
    print("Threshold Alerts:")
    print(json.dumps(threshold_alert_json, indent=4))

    # Save threshold alerts JSON to file
    save_json_output(threshold_alert_json, output_path, "threshold_alerts")

    logging.info("Log analysis completed successfully")

if __name__ == "__main__":
    main()
