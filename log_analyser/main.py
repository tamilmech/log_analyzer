import logging
import os
import pandas as pd
import json
from logs_preprocessor import LogParser
from model_components.SentimentAnalysis import SentimentAnalysis
from model_components.log_sensitive_data_parser import SensitiveDataParser
from model_components.clustering_keywords import KeywordClustering
from model_components.AnomalyPrediction import AnomalyPrediction
from model_components.Root_Cause_Analysis import RootCauseAnalysis
from model_components.Threshold_Alert import ThresholdAlert
from model_components.DBSCAN_Clustering import DBSCANClustering
from model_components.HDBSCAN_Clustering import HDBSCANClustering
from Plot_Analysis import LogLevelVisualizer, SentimentVisualizer, KeywordClusteringVisualizer

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
    csv_path = os.path.join(output_path, f"{filename}.csv")
    df.to_csv(csv_path, index=False)
    logging.info(f"Saved CSV output: {csv_path}")

    json_path = os.path.join(output_path, f"{filename}.json")
    df.to_json(json_path, orient="records", lines=True)
    logging.info(f"Saved JSON output: {json_path}")

def save_json_output(data, output_path, filename):
    """
    Save JSON output to the given path, ensuring proper formatting.
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON string: {e}")
            return

    json_path = os.path.join(output_path, f"{filename}.json")
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    logging.info(f"Saved JSON output: {json_path}")

def main():
    logging.info("Starting log analysis")

    # Define paths
    log_file_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/logs_data/data_logs.txt"
    output_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/model_outputs"
    error_visualization_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/visualization/error_level"
    sentiment_visualization_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/visualization/sentimental_analysis"
    keyword_clustering_visualization_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/visualization/keyword_clustering"

    os.makedirs(output_path, exist_ok=True)

    # Log parsing
    log_parser = LogParser()
    df = log_parser.parse(log_file_path)
    if df.empty:
        logging.warning("No valid logs to display.")
        return

    # Ensure timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    # Save parsed logs
    save_output(df, output_path, "parsed_logs")

    # Log level visualizations
    log_level_visualizer = LogLevelVisualizer(df, error_visualization_path)
    log_level_visualizer.run_visualizations()

    # Sentiment Analysis
    sentiment_analyzer = SentimentAnalysis()
    sentiment_df = sentiment_analyzer.analyze(df)
    save_output(sentiment_df, output_path, "sentiment_analysis_results")

    sentiment_visualizer = SentimentVisualizer(sentiment_df, sentiment_visualization_path)
    sentiment_visualizer.run_visualizations()

    # Sensitive Data Parsing
    sensitive_data_parser = SensitiveDataParser()
    sensitive_data = sensitive_data_parser.parse(df)
    save_json_output(sensitive_data, output_path, "sensitive_data")

    # Keyword Clustering
    keyword_clustering = KeywordClustering()
    clustered_df = keyword_clustering.categorize(df)
    save_output(clustered_df, output_path, "keyword_clustering_results")

    keyword_clustering_visualizer = KeywordClusteringVisualizer(clustered_df, keyword_clustering_visualization_path)
    keyword_clustering_visualizer.run_visualizations()

    # Anomaly Detection
    anomaly_predictor = AnomalyPrediction()
    anomalies_json = anomaly_predictor.analyze(df)
    structured_data = json.loads(anomalies_json) if isinstance(anomalies_json, str) else anomalies_json
    save_json_output(structured_data, output_path, "anomalies")

    # Root Cause Analysis
    root_cause_analyzer = RootCauseAnalysis()
    root_cause_json = root_cause_analyzer.analyze(structured_data)
    save_json_output(root_cause_json, output_path, "root_cause_analysis")

    # Threshold Alert Analysis
    threshold_alert = ThresholdAlert()
    threshold_alert_json = threshold_alert.analyze(structured_data)
    save_json_output(threshold_alert_json, output_path, "threshold_alerts")

    # DBSCAN Clustering (if needed)
    dbscan_clustering = DBSCANClustering()
    dbscan_results = dbscan_clustering.cluster(df)
    save_output(dbscan_results, output_path, "dbscan_clustering_results")

    # HDBSCAN Clustering (if needed)
    hdbscan_clustering = HDBSCANClustering()
    hdbscan_results = hdbscan_clustering.cluster(df)
    save_output(hdbscan_results, output_path, "hdbscan_clustering_results")

    logging.info("Log analysis completed successfully")

if __name__ == "__main__":
    main()
