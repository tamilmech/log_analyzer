import os
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image
from langchain_groq import ChatGroq
from config.paths import MainPath

# Paths to folders
folder_path = f"{MainPath.folder_path}/log_analyser/model_outputs"
error_level_path = f"{MainPath.folder_path}/log_analyser/visualization/error_level"
keyword_clustering_path = f"{MainPath.folder_path}/log_analyser/visualization/keyword_clustering"
sentimental_analysis_path = f"{MainPath.folder_path}/log_analyser/visualization/sentimental_analysis"
sentiment_output_path = os.path.join(folder_path, "sentiment_analysis_results.csv")

# Google Search Function
def google_search(query, num_results=5):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for g in soup.find_all('div', class_='tF2Cxc')[:num_results]:  # Adjust result limit
            link = g.find('a')['href']
            title = g.find('h3').text
            results.append({'title': title, 'link': link})
        return results
    else:
        return None

# Create a list of pages as buttons
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", ["Troubleshooting", "Google Search Results", "Plots and DataFrames"])

if selected_page == "Troubleshooting":
    st.title("Troubleshooting Guide (LangChain)")
    st.markdown("---")

    # Load the sentiment analysis CSV
    try:
        sentiment_df = pd.read_csv(sentiment_output_path)
    except Exception as e:
        st.error(f"Error loading sentiment analysis file: {e}")
        st.stop()

    # Filter messages where Sentiment is "Negative" and Confidence >= 0.50
    filtered_messages = sentiment_df[
        (sentiment_df["Sentiment"] == "Negative") & (sentiment_df["Confidence"] >= 0.50)
    ]["message"]

    if filtered_messages.empty:
        st.warning("No negative sentiment messages with high confidence found.")
    else:
        # Initialize LangChain ChatGroq model
        llm = ChatGroq(
            temperature=0,
            groq_api_key="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",  # Replace with your actual API key
            model_name="llama-3.1-70b-versatile"  # Replace with desired model
        )

        for idx, message in enumerate(filtered_messages, start=1):
            st.subheader(f"Error {idx}:")
            st.write(f"**Error Message:** {message}")

            try:
                # LangChain: Pass the error message to the model
                langchain_response = llm.invoke(f"What is this error, and how to solve it?:\n{message}")
                st.markdown(
                    f"""
                    <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
                        <strong>LangChain Solution:</strong> {langchain_response.content}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Error processing message with LangChain: {e}")

elif selected_page == "Google Search Results":
    st.title("Google Search Results for Errors")
    st.markdown("---")

    # Load the sentiment analysis CSV
    try:
        sentiment_df = pd.read_csv(sentiment_output_path)
    except Exception as e:
        st.error(f"Error loading sentiment analysis file: {e}")
        st.stop()

    # Filter messages where Sentiment is "Negative" and Confidence >= 0.50
    filtered_messages = sentiment_df[
        (sentiment_df["Sentiment"] == "Negative") & (sentiment_df["Confidence"] >= 0.50)
    ]["message"]

    if filtered_messages.empty:
        st.warning("No negative sentiment messages with high confidence found.")
    else:
        for idx, message in enumerate(filtered_messages, start=1):
            st.subheader(f"Error {idx}:")
            st.write(f"**Error Message:** {message}")

            # Google Search: Perform search for the error message
            google_results = google_search(message)

            if google_results:
                st.markdown("### Top Solutions from Google:")
                for result_idx, result in enumerate(google_results, start=1):
                    st.markdown(f"**{result_idx}.** [{result['title']}]({result['link']})")
            else:
                st.error("Failed to retrieve search results from Google.")

            # Add spacing between each error
            st.markdown("<br>", unsafe_allow_html=True)

elif selected_page == "Plots and DataFrames":
    st.title("Log Analyzer Outputs Viewer")
    st.markdown("---")

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
