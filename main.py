from logs_preprocessor import LogParser
from model_components.model_loader import SentimentAnalysis

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

    # Display the results
    print("Analyzed Logs:")
    print(analyzed_df[['message','Sentiment']])

if __name__ == "__main__":
    main()
