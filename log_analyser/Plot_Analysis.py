import os
import logging
import matplotlib.pyplot as plt
import pandas as pd


# -------------------------------------------------------------------
#                   Log Level Visualizer
# -------------------------------------------------------------------
class LogLevelVisualizer:
    """
    A visualizer for log level data, providing bar and line chart visualizations.
    """

    def __init__(self, log_df: pd.DataFrame, output_path: str):
        """
        Initialize the LogLevelVisualizer with log DataFrame and output directory.

        :param log_df: DataFrame containing log data.
        :param output_path: Path to save visualizations.
        """
        self.log_df = log_df
        self.output_path = output_path

    def generate_log_level_barchart(self) -> None:
        """
        Generate a bar chart for log levels with specific colors for 'INFO' and 'ERROR'.
        Saves the chart as 'log_levels_barchart.png' in the output directory.
        """
        os.makedirs(self.output_path, exist_ok=True)
        level_counts = self.log_df['level'].value_counts()

        colors = ['green' if level == 'INFO' else 'red' for level in level_counts.index]
        plt.figure(figsize=(10, 6))
        bars = plt.bar(level_counts.index, level_counts.values, color=colors, edgecolor='black')
        plt.title("Log Levels Count", fontsize=16, weight='bold')
        plt.xlabel("Log Level", fontsize=12)
        plt.ylabel("Count", fontsize=12)

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height() + 0.5,
                str(bar.get_height()),
                ha='center',
                va='bottom',
                fontsize=10,
                color='black',
                weight='bold',
            )

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_path, "log_levels_barchart.png"))
        plt.close()

    def generate_error_hourly_linechart(self) -> None:
        """
        Generate a line chart for hourly error counts.
        Saves the chart as 'error_hourly_linechart.png' in the output directory.
        """
        error_data = self.log_df[self.log_df['level'] == 'ERROR'].copy()
        error_data['hour'] = error_data['timestamp'].dt.floor('h')
        hourly_error_counts = error_data['hour'].value_counts().sort_index()

        plt.figure(figsize=(12, 6))
        plt.plot(
            hourly_error_counts.index,
            hourly_error_counts.values,
            marker='o',
            linestyle='-',
            linewidth=2,
            color='crimson',
        )
        plt.title("Error Count by Hour", fontsize=16, weight='bold')
        plt.xlabel("Hour", fontsize=12)
        plt.ylabel("Error Count", fontsize=12)
        plt.grid(axis='both', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_path, "error_hourly_linechart.png"))
        plt.close()

    def run_visualizations(self) -> None:
        """
        Run all visualizations for log level data.
        """
        self.generate_log_level_barchart()
        self.generate_error_hourly_linechart()


# -------------------------------------------------------------------
#                   Sentiment Visualizer
# -------------------------------------------------------------------
class SentimentVisualizer:
    """
    A visualizer for sentiment analysis data, providing bar chart visualizations.
    """

    def __init__(self, sentiment_df: pd.DataFrame, output_path: str):
        """
        Initialize the SentimentVisualizer with sentiment DataFrame and output directory.

        :param sentiment_df: DataFrame containing sentiment analysis data.
        :param output_path: Path to save visualizations.
        """
        self.sentiment_df = sentiment_df
        self.output_path = output_path

    def generate_sentiment_barchart(self) -> None:
        """
        Generate a bar chart for sentiment distribution.
        Saves the chart as 'sentiment_barchart.png' in the output directory.
        """
        os.makedirs(self.output_path, exist_ok=True)
        sentiment_counts = self.sentiment_df['Sentiment'].value_counts()

        colors = ['green' if sentiment == 'Positive' else 'red' if sentiment == 'Negative' else 'blue'
                  for sentiment in sentiment_counts.index]
        plt.figure(figsize=(10, 6))
        bars = plt.bar(sentiment_counts.index, sentiment_counts.values, color=colors, edgecolor='black')
        plt.title("Sentiment Distribution", fontsize=16, weight='bold')
        plt.xlabel("Sentiment", fontsize=12)
        plt.ylabel("Count", fontsize=12)

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height() + 0.5,
                str(bar.get_height()),
                ha='center',
                va='bottom',
                fontsize=10,
                color='black',
                weight='bold',
            )

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_path, "sentiment_barchart.png"))
        plt.close()

    def run_visualizations(self) -> None:
        """
        Run all visualizations for sentiment analysis data.
        """
        self.generate_sentiment_barchart()


# -------------------------------------------------------------------
#                   Keyword Clustering Visualizer
# -------------------------------------------------------------------
class KeywordClusteringVisualizer:
    """
    A visualizer for keyword clustering data, providing bar chart visualizations.
    """

    def __init__(self, clustered_df: pd.DataFrame, output_path: str):
        """
        Initialize the KeywordClusteringVisualizer with clustering DataFrame and output directory.

        :param clustered_df: DataFrame containing keyword clustering data.
        :param output_path: Path to save visualizations.
        """
        self.clustered_df = clustered_df
        self.output_path = output_path

    def generate_keyword_barchart(self) -> None:
        """
        Generate a bar chart for keyword clusters (filtered by 'ERROR' level).
        Saves the chart as 'keyword_cluster_barchart.png' in the output directory.
        """
        os.makedirs(self.output_path, exist_ok=True)
        error_clusters = self.clustered_df[self.clustered_df['level'] == 'ERROR']
        cluster_counts = error_clusters['Keyword_cluster'].value_counts()

        plt.figure(figsize=(10, 6))
        bars = plt.bar(cluster_counts.index, cluster_counts.values, color='orange', edgecolor='black')
        plt.title("Keyword Cluster Distribution (Errors Only)", fontsize=16, weight='bold')
        plt.xlabel("Cluster", fontsize=12)
        plt.ylabel("Count", fontsize=12)

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height() + 0.5,
                str(bar.get_height()),
                ha='center',
                va='bottom',
                fontsize=10,
                color='black',
                weight='bold',
            )

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_path, "keyword_cluster_barchart.png"))
        plt.close()

    def run_visualizations(self) -> None:
        """
        Run all visualizations for keyword clustering data.
        """
        self.generate_keyword_barchart()
