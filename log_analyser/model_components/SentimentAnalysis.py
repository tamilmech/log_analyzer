from transformers import pipeline
import torch
import pandas as pd

# -------------------------------------------------------------------
#                   Sentiment Analysis
# -------------------------------------------------------------------

class SentimentAnalysis:
    """
    A class to analyze the sentiment of log messages using PyTorch and transformers.
    """

    def __init__(self):
        """
            https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment
        """
        
        """
        Initialize the SentimentAnalysis class by loading a pre-trained sentiment analysis model.

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

    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze sentiment for a given DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing a 'message' column.

        Returns:
            pd.DataFrame: DataFrame with 'Sentiment' and 'Confidence' columns added.

        Raises:
            ValueError: If the DataFrame does not contain the required 'message' column.

        FIXME: Optimize keyword embeddings for better performance in edge cases and ambiguous messages.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        sentiments: list[str] = []
        confidences: list[float] = []

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
