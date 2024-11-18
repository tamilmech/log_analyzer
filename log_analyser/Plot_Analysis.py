import os
import logging
import matplotlib.pyplot as plt
import pandas as pd


class LogLevelVisualizer:
    def __init__(self, log_df, output_path):
        self.log_df = log_df
        self.output_path = output_path

    def generate_log_level_barchart(self):
        """
        Generate a bar chart for log levels with specific colors for 'INFO' and 'ERROR'.
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

    def generate_error_hourly_linechart(self):
        """
        Generate a line chart for hourly error counts.
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

    def run_visualizations(self):
        self.generate_log_level_barchart()
        self.generate_error_hourly_linechart()


class SentimentVisualizer:
    def __init__(self, sentiment_df, output_path):
        self.sentiment_df = sentiment_df
        self.output_path = output_path

    def generate_sentiment_barchart(self):
        """
        Generate a bar chart for sentiment analysis with custom colors.
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

    def run_visualizations(self):
        self.generate_sentiment_barchart()


class KeywordClusteringVisualizer:
    def __init__(self, clustered_df, output_path):
        self.clustered_df = clustered_df
        self.output_path = output_path

    def generate_keyword_barchart(self):
        """
        Generate a bar chart for keyword clusters (filtered by 'ERROR' level).
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

    def run_visualizations(self):
        self.generate_keyword_barchart()
