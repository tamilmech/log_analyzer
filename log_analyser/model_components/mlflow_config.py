from transformers import pipeline
import torch
import pandas as pd
import mlflow
import mlflow.pyfunc

# -------------------------------------------------------------------
#                   Sentiment Analysis with MLflow
# -------------------------------------------------------------------

class SentimentAnalysis:
    """
    A class to analyze the sentiment of log messages using PyTorch and transformers.
    """

    def __init__(self, tracking_uri: str = "mlruns"):
        """
        Initialize the SentimentAnalysis class by loading a pre-trained sentiment analysis model
        and setting up MLflow tracking.

        Args:
            tracking_uri (str): MLflow tracking URI.

        TODO: This transformer is lightweight, but GPU settings need to be explicitly specified.
              Plan to add advanced transformer pipelines for better accuracy and performance.
        """
        # Explicitly use PyTorch and determine device (GPU if available)
        self.device: int = 0 if torch.cuda.is_available() else -1
        self.classifier = pipeline(
            "sentiment-analysis", 
            model="nlptown/bert-base-multilingual-uncased-sentiment", 
            framework="pt", 
            device=self.device
        )

        # Set up MLflow tracking
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment("Sentiment Analysis Experiment")

    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze sentiment for a given DataFrame and log the results with MLflow.

        Args:
            df (pd.DataFrame): DataFrame containing a 'message' column.

        Returns:
            pd.DataFrame: DataFrame with 'Sentiment' and 'Confidence' columns added.

        Raises:
            ValueError: If the DataFrame does not contain the required 'message' column.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        sentiments: list[str] = []
        confidences: list[float] = []

        with mlflow.start_run():
            # Log parameter: model name
            mlflow.log_param("model", "nlptown/bert-base-multilingual-uncased-sentiment")
            mlflow.log_param("device", "GPU" if self.device == 0 else "CPU")

            # Analyze each message in the DataFrame
            for message in df['message']:
                result = self.classifier(message)[0]

                # Map model output to Positive, Neutral, or Negative
                if "1 star" in result['label'] or "2 stars" in result['label']:
                    sentiment = "Negative"
                elif "4 stars" in result['label'] or "5 stars" in result['label']:
                    sentiment = "Positive"
                else:
                    sentiment = "Neutral"  # Optional for 3 stars or uncertain cases

                sentiments.append(sentiment)
                confidences.append(result['score'])

            # Add sentiment and confidence to the DataFrame
            df['Sentiment'] = sentiments
            df['Confidence'] = confidences

            # Log metrics
            positive_count = sentiments.count("Positive")
            negative_count = sentiments.count("Negative")
            neutral_count = sentiments.count("Neutral")
            mlflow.log_metric("Positive Sentiments", positive_count)
            mlflow.log_metric("Negative Sentiments", negative_count)
            mlflow.log_metric("Neutral Sentiments", neutral_count)

            # Log the resulting DataFrame as an artifact
            result_file = "sentiment_analysis_results.csv"
            df.to_csv(result_file, index=False)
            mlflow.log_artifact(result_file)

            return df


# -------------------------------------------------------------------
#                   Main Execution
# -------------------------------------------------------------------

if __name__ == "__main__":
    """
    Main block for testing the SentimentAnalysis class with sample data.
    """
    sample_data = {
        "message": [
            "The service started successfully.",
            "Failed to connect to the database.",
            "Warning: Disk space is running low.",
            "The transaction was completed.",
        ]
    }
    df = pd.DataFrame(sample_data)
    sentiment_analyzer = SentimentAnalysis()
    analyzed_df = sentiment_analyzer.analyze(df)
    print(analyzed_df)
