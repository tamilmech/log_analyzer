import pandas as pd

class KeywordClustering:
    """
    A class to categorize log messages into predefined keyword-based categories.
    """
    def __init__(self):
        # Define the categories with keywords
        self.categories = {
            "kafka": ["partition", "zookeeper", "producer", "consumer", "topic"],
            "python": ["list index out of range", "no module", "indentation", "syntax error", "TypeError"],
            "airflow": ["DAG", "task", "scheduler", "trigger", "sensor"],
            "aws": ["AccessDenied", "ThrottlingException", "Lambda", "S3", "API Gateway"],
            "database": ["query", "transaction", "rollback", "VACUUM", "deadlock", "database"],
            "api": ["endpoint", "HTTP method", "status code", "unauthorized", "404 Not Found",
                    "Internal Server Error", "PUT", "DELETE", "GET", "api"],
            "server": ["CPU", "memory", "disk", "timeout", "GC overhead"],
            "logging": ["logged"]
        }

    def categorize(self, df):
        """
        Categorize the log messages into keyword-based categories.

        Args:
            df (pd.DataFrame): DataFrame containing a 'message' column.

        Returns:
            pd.DataFrame: A new DataFrame with an added 'Keyword_cluster' column.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        # Categorize messages based on keywords
        df["Keyword_cluster"] = df["message"].apply(self.categorize_message)
        return df

    def categorize_message(self, message):
        """
        Categorize a single message based on keywords.

        Args:
            message (str): The log message.

        Returns:
            str: The category of the message.
        """
        for category, keywords in self.categories.items():
            if any(keyword.lower() in message.lower() for keyword in keywords):
                return category
        return "unknown"  # Default if no category matches
