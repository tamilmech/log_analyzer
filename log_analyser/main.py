from contextlib import redirect_stdout

from logs_preprocessor import LogParser
from model_components.model_loader import SentimentAnalysis
from model_components.log_sensitive_data_parser import SensitiveDataParser
from model_components.clustering_keywords import KeywordClustering
from model_components.AnomalyPrediction import AnomalyPrediction
from model_components.Root_Cause_Analysis import RootCauseAnalysis
from model_components.Threshold_Alert import ThresholdAlert
from model_components.DBSCAN_Clustering import DBSCANClustering
from model_components.HDBSCAN_Clustering import HDBSCANClustering
#from model_components.Cluster_Title import ClusterTitleGenerator  # Import the ClusterTitleGenerator class

import json

def main():
    # Define the path to the sample log file
    log_file_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/logs_data/data_logs.txt"  # Replace with the actual path to your log file

    # Initialize the LogParser
    log_parser = LogParser()

    # Parse the log file
    df = log_parser.parse(log_file_path)
    print(df[['level','message']])

    # Check if the DataFrame is empty
    if df.empty:
        print("No valid logs to display.")
        return

    # Initialize the SentimentAnalysis class
    sentiment_analyzer = SentimentAnalysis()

    # Analyze the sentiment of the messages
    analyzed_df = sentiment_analyzer.analyze(df)

    # Display the sentiment analysis results
    print("Analyzed Logs:")
    print(analyzed_df[['message', 'Sentiment']])

    # Initialize the SensitiveDataParser
    sensitive_data_parser = SensitiveDataParser()

    # Parse sensitive data
    sensitive_data = sensitive_data_parser.parse(df)

    # Display parsed sensitive data as JSON
    print("Parsed Sensitive Data:")
    print(json.dumps(sensitive_data, indent=4))

    # Initialize the KeywordClustering class
    keyword_clustering = KeywordClustering()

    # Categorize the messages into clusters
    clustered_df = keyword_clustering.categorize(df)

    # Display the clustering results
    print("Clustered Logs:")
    print(clustered_df[['message', 'Keyword_cluster']])

    # Initialize the AnomalyPrediction class
    anomaly_predictor = AnomalyPrediction()

    # Extract specific metrics and failure events
    anomalies_json = anomaly_predictor.analyze(df)

    # Display the anomalies as JSON
    print("Extracted Anomalies:")
    print(anomalies_json)

    # Convert anomalies JSON back to a Python object for threshold alert analysis
    structured_data = json.loads(anomalies_json)

    # Initialize the RootCauseAnalysis class
    root_cause_analyzer = RootCauseAnalysis()

    # Analyze the root causes and provide recommendations
    root_cause_json = root_cause_analyzer.analyze(structured_data)

    # Display the root causes and recommendations
    print("Root Causes and Recommendations:")
    print(root_cause_json)

    # Initialize the ThresholdAlert class
    threshold_alert = ThresholdAlert()

    # Analyze the thresholds and provide alerts
    threshold_alert_json = threshold_alert.analyze(structured_data)

    # Display threshold alerts
    print("Threshold Alerts:")
    print(threshold_alert_json)

    # Initialize the DBSCANClustering class
    dbscan_clustering = DBSCANClustering()

    # Cluster the log messages using DBSCAN
    dbscan_clustered_df = dbscan_clustering.cluster(df)

    # Display the DBSCAN clustering results
    print("DBSCAN Clustering Results:")
    print(dbscan_clustered_df[['message', 'cluster']])

    # Group logs by cluster
    for cluster_id in dbscan_clustered_df['cluster'].unique():
        print(f"\nCluster {cluster_id}:")
        print(dbscan_clustered_df[dbscan_clustered_df['cluster'] == cluster_id]['message'])

    # Initialize the HDBSCANClustering class
    hdbscan_clustering = HDBSCANClustering()

    # Cluster the log messages using HDBSCAN
    hdbscan_clustered_df = hdbscan_clustering.cluster(df)

    # Display the HDBSCAN clustering results
    print("HDBSCAN Clustering Results:")
    print(hdbscan_clustered_df)

    # Initialize the ClusterTitleGenerator class
    #cluster_title_generator = ClusterTitleGenerator()

    # Generate cluster titles and counts
    #cluster_titles_df = cluster_title_generator.generate_titles(dbscan_clustered_df)

    # Display the cluster titles
    #print("Cluster Titles and Counts:")
    #print(cluster_titles_df)

if __name__ == "__main__":
    #main()
    
    # Save output to a file
    with open("logs_analyser_output.txt", "w") as output_file:
        with redirect_stdout(output_file):
            main()
