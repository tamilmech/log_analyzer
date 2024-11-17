from logs_preprocessor import LogParser
from model_components.model_loader import SentimentAnalysis
from model_components.log_sensitive_data_parser import SensitiveDataParser  # Import the new class

import json
def main():
    # Define the path to the sample log file
    log_file_path = "/Users/tamilselavans/Desktop/log_analyzer/log_analyser/logs_data/data_logs.txt"  # Replace with the actual path to your log file

    # Initialize the LogParser
    log_parser = LogParser()

    # Parse the log file
    df = log_parser.parse(log_file_path)

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

if __name__ == "__main__":
    main()
