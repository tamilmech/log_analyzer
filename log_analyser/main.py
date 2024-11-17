import logging
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
# from model_components.Cluster_Title import ClusterTitleGenerator  # Import the ClusterTitleGenerator class

import json

# Configure logging
logging.basicConfig(
    filename="log_analyzer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    logging.info("Starting log analysis")

    # Define the path to the sample log file
    log_file_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/logs_data/data_logs.txt"  # Replace with the actual path to your log file
    logging.info(f"Log file path: {log_file_path}")

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

    # Initialize the SentimentAnalysis class
    logging.info("Initializing SentimentAnalysis")
    sentiment_analyzer = SentimentAnalysis()

    # Analyze the sentiment of the messages
    logging.info("Analyzing sentiment of log messages")
    analyzed_df = sentiment_analyzer.analyze(df)
    logging.info("Sentiment analysis completed")
    print("Analyzed Logs:")
    print(analyzed_df[['message', 'Sentiment']])

    # Initialize the SensitiveDataParser
    logging.info("Initializing SensitiveDataParser")
    sensitive_data_parser = SensitiveDataParser()

    # Parse sensitive data
    logging.info("Parsing sensitive data")
    sensitive_data = sensitive_data_parser.parse(df)
    logging.info("Sensitive data parsing completed")
    print("Parsed Sensitive Data:")
    print(json.dumps(sensitive_data, indent=4))

    # Initialize the KeywordClustering class
    logging.info("Initializing KeywordClustering")
    keyword_clustering = KeywordClustering()

    # Categorize the messages into clusters
    logging.info("Clustering messages into categories")
    clustered_df = keyword_clustering.categorize(df)
    logging.info("Keyword clustering completed")
    print("Clustered Logs:")
    print(clustered_df[['message', 'Keyword_cluster']])

    # Initialize the AnomalyPrediction class
    logging.info("Initializing AnomalyPrediction")
    anomaly_predictor = AnomalyPrediction()

    # Extract specific metrics and failure events
    logging.info("Extracting anomalies from log messages")
    anomalies_json = anomaly_predictor.analyze(df)
    logging.info("Anomaly prediction completed")
    print("Extracted Anomalies:")
    print(anomalies_json)

    # Convert anomalies JSON back to a Python object for threshold alert analysis
    structured_data = json.loads(anomalies_json)

    # Initialize the RootCauseAnalysis class
    logging.info("Initializing RootCauseAnalysis")
    root_cause_analyzer = RootCauseAnalysis()

    # Analyze the root causes and provide recommendations
    logging.info("Analyzing root causes")
    root_cause_json = root_cause_analyzer.analyze(structured_data)
    logging.info("Root cause analysis completed")
    print("Root Causes and Recommendations:")
    print(root_cause_json)

    # Initialize the ThresholdAlert class
    logging.info("Initializing ThresholdAlert")
    threshold_alert = ThresholdAlert()

    # Analyze the thresholds and provide alerts
    logging.info("Analyzing thresholds for alerts")
    threshold_alert_json = threshold_alert.analyze(structured_data)
    logging.info("Threshold alert analysis completed")
    print("Threshold Alerts:")
    print(threshold_alert_json)

    # Initialize the DBSCANClustering class
    logging.info("Initializing DBSCANClustering")
    dbscan_clustering = DBSCANClustering()

    # Cluster the log messages using DBSCAN
    logging.info("Clustering log messages using DBSCAN")
    dbscan_clustered_df = dbscan_clustering.cluster(df)
    logging.info("DBSCAN clustering completed")
    print("DBSCAN Clustering Results:")
    print(dbscan_clustered_df[['message', 'cluster']])

    # Group logs by cluster
    logging.info("Grouping logs by DBSCAN clusters")
    for cluster_id in dbscan_clustered_df['cluster'].unique():
        print(f"\nCluster {cluster_id}:")
        print(dbscan_clustered_df[dbscan_clustered_df['cluster'] == cluster_id]['message'])

    # Initialize the HDBSCANClustering class
    logging.info("Initializing HDBSCANClustering")
    hdbscan_clustering = HDBSCANClustering()

    # Cluster the log messages using HDBSCAN
    logging.info("Clustering log messages using HDBSCAN")
    hdbscan_clustered_df = hdbscan_clustering.cluster(df)
    logging.info("HDBSCAN clustering completed")
    print("HDBSCAN Clustering Results:")
    print(hdbscan_clustered_df)

    # Uncomment if ClusterTitleGenerator is implemented
    # logging.info("Initializing ClusterTitleGenerator")
    # cluster_title_generator = ClusterTitleGenerator()
    # cluster_titles_df = cluster_title_generator.generate_titles(dbscan_clustered_df)
    # logging.info("Cluster title generation completed")
    # print("Cluster Titles and Counts:")
    # print(cluster_titles_df)

    logging.info("Log analysis completed successfully")

if __name__ == "__main__":
    main()
