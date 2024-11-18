from transformers import pipeline
import torch
import pandas as pd

class SentimentAnalysis:
    """
    A class to analyze the sentiment of log messages using PyTorch.
    """
    def __init__(self):
        # Explicitly use PyTorch
        self.device = 0 if torch.cuda.is_available() else -1
        self.classifier = pipeline(
            "sentiment-analysis", 
            model="nlptown/bert-base-multilingual-uncased-sentiment", 
            framework="pt", 
            device=self.device
        )

    def analyze(self, df):
        """
        Analyze sentiment for a given DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing a 'message' column.

        Returns:
            pd.DataFrame: DataFrame with 'Sentiment' and 'Confidence' columns added.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        sentiments = []
        confidences = []

        for message in df['message']:
            result = self.classifier(message)[0]

            # Map model output to Positive or Negative
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

if __name__ == "__main__":
    # For testing purposes
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