import os
import pandas as pd
import json
import streamlit as st
from PIL import Image
from langchain_groq import ChatGroq
from config.paths import MainPath 
# Paths to folders
folder_path = f"{MainPath.folder_path}/log_analyser/model_outputs"
error_level_path = f"{MainPath.folder_path}/log_analyser/visualization/error_level"
keyword_clustering_path = f"{MainPath.folder_path}/log_analyser/visualization/keyword_clustering"
sentimental_analysis_path = f"{MainPath.folder_path}/log_analyser/visualization/sentimental_analysis"

# Create a list of pages as buttons
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", ["Troubleshooting", "Plots and DataFrames"])

if selected_page == "Troubleshooting":
    st.title("Troubleshooting Guide (LangChain)")
    st.markdown("---")  # Add a horizontal line for separation

    # Path to the saved sentiment analysis CSV
    sentiment_output_path = os.path.join(folder_path, "sentiment_analysis_results.csv")

    # Load the CSV file as a DataFrame
    try:
        sentiment_df = pd.read_csv(sentiment_output_path)
    except Exception as e:
        st.error(f"Error loading sentiment analysis file: {e}")
        st.stop()

    # Filter messages where Sentiment is "Negative" and Confidence >= 0.70
    filtered_messages = sentiment_df[
        (sentiment_df["Sentiment"] == "Negative") & (sentiment_df["Confidence"] >= 0.70)
    ]["message"]

    if filtered_messages.empty:
        st.warning("No negative sentiment messages with high confidence found.")
    else:
        # Initialize ChatGroq with your API key and model name
        llm = ChatGroq(
            temperature=0,
            groq_api_key="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",  # Replace with your actual API key
            model_name="llama-3.1-70b-versatile"  # Model name
        )

        for idx, message in enumerate(filtered_messages, start=1):
            # Assign the message to the error variable
            error = message
            st.subheader(f"Error {idx}:")
            st.write(f"**Error Message:** {error}")

            try:
                # Pass the error message to the model
                response = llm.invoke(f"What is this error, and how to solve it?:\n{error}")

                # Display the model's response with colored background
                st.markdown(
                    f"""
                    <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
                        <strong>Solution:</strong> {response.content}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Error processing message: {e}")

            # Add spacing between each error
            st.markdown("<br>", unsafe_allow_html=True)

elif selected_page == "Plots and DataFrames":
    st.title("Log Analyzer Outputs Viewer")
    st.markdown("---")  # Add a horizontal line for separation

    # List all files in the main data directory
    files = os.listdir(folder_path)
    json_files = [file for file in files if file.endswith(".json")]
    csv_files = [file for file in files if file.endswith(".csv")]

    # List all PNGs in visualization folders
    error_images = [os.path.join(error_level_path, img) for img in os.listdir(error_level_path) if img.endswith(".png")]
    keyword_images = [os.path.join(keyword_clustering_path, img) for img in os.listdir(keyword_clustering_path) if img.endswith(".png")]
    sentiment_images = [os.path.join(sentimental_analysis_path, img) for img in os.listdir(sentimental_analysis_path) if img.endswith(".png")]

    # Function to display file content
    def display_file(file_path):
        if file_path.endswith(".json"):
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    try:
                        data = json.loads(content)  # Attempt to load full JSON
                        st.json(data)
                    except json.JSONDecodeError:
                        st.warning("File contains multiple JSON objects. Displaying each object.")
                        for line in content.splitlines():
                            if line.strip():
                                try:
                                    data = json.loads(line)
                                    st.json(data)
                                except json.JSONDecodeError:
                                    st.error(f"Invalid JSON line: {line}")
            except Exception as e:
                st.error(f"Error reading JSON file: {e}")
        elif file_path.endswith(".csv"):
            try:
                df = pd.read_csv(file_path)
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error loading CSV file: {e}")

    # Display JSON and CSV files in tabs
    if json_files or csv_files:
        st.header("JSON and CSV Outputs")
        file_tabs = st.tabs([os.path.splitext(file)[0] for file in (csv_files + json_files)])
        for idx, file in enumerate(csv_files + json_files):
            with file_tabs[idx]:
                file_path = os.path.join(folder_path, file)
                st.subheader(f"File: {file}")
                display_file(file_path)
    else:
        st.write("No JSON or CSV files found in the specified directory.")

    # Function to display images
    def display_images(image_paths, title):
        st.header(title)
        for img_path in image_paths:
            st.subheader(os.path.basename(img_path))
            image = Image.open(img_path)
            st.image(image, use_column_width=True)

    # Display PNG images from visualization folders
    if error_images:
        display_images(error_images, "Error Level Visualizations")

    if keyword_images:
        display_images(keyword_images, "Keyword Clustering Visualizations")

    if sentiment_images:
        display_images(sentiment_images, "Sentimental Analysis Visualizations")
