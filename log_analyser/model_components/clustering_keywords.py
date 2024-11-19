import pandas as pd

# -------------------------------------------------------------------
#                   Keyword Clustering
# -------------------------------------------------------------------

class KeywordClustering:
    """
    A class to categorize log messages into predefined keyword-based categories.
    """

    def __init__(self):
        """
        Initialize the KeywordClustering class with predefined keyword-based categories.

        TODO: Need to add more components to improve clustering accuracy.
        """
        # Define the categories with associated keywords
        self.categories: dict[str, list[str]] = {
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

    def categorize(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize the log messages into keyword-based categories.

        Args:
            df (pd.DataFrame): DataFrame containing a 'message' column.

        Returns:
            pd.DataFrame: A new DataFrame with an added 'Keyword_cluster' column.

        Raises:
            ValueError: If the DataFrame does not contain the 'message' column.

        TODO: Add a confidence column using transformer pipelines to assess the strength of matches.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        # Categorize each message and add the category to a new column
        df["Keyword_cluster"] = df["message"].apply(self.categorize_message)
        return df

    def categorize_message(self, message: str) -> str:
        """
        Categorize a single log message based on predefined keywords.

        Args:
            message (str): The log message.

        Returns:
            str: The category of the message. Returns 'unknown' if no category matches.

        TODO: Enhance the categorization by integrating advanced NLP models for better accuracy.
        """
        for category, keywords in self.categories.items():
            # Check if any keyword matches the message
            if any(keyword.lower() in message.lower() for keyword in keywords):
                return category
        return "unknown"  # Default category if no match is found
