from keybert import KeyBERT
import pandas as pd


class ClusterTitleGenerator:
    """
    A class to generate titles for clusters using KeyBERT.
    """

    def __init__(self):
        """
        Initialize the KeyBERT model.
        """
        self.kw_model = KeyBERT()

    def generate_titles(self, df):
        """
        Generate cluster titles and counts.

        Args:
            df (pd.DataFrame): DataFrame containing 'cluster' and 'message' columns.

        Returns:
            pd.DataFrame: A DataFrame summarizing cluster IDs, titles, and message counts.
        """
        if "cluster" not in df.columns or "message" not in df.columns:
            raise ValueError("The DataFrame must contain 'cluster' and 'message' columns.")

        # Dictionary to store cluster titles and counts
        cluster_data = []

        # Generate cluster titles and counts
        for cluster_id in df['cluster'].unique():
            cluster_messages = df[df['cluster'] == cluster_id]['message']
            combined_text = " ".join(cluster_messages)

            if combined_text.strip():  # Skip empty clusters
                key_phrases = self.kw_model.extract_keywords(combined_text, keyphrase_ngram_range=(1, 2), stop_words='english')
                cluster_title = ", ".join([phrase[0] for phrase in key_phrases[:3]])  # Top 3 phrases
            else:
                cluster_title = "No meaningful messages in this cluster"

            # Append cluster data
            cluster_data.append({
                "Cluster ID": cluster_id,
                "Title": cluster_title,
                "Message Count": len(cluster_messages)
            })

        # Convert to DataFrame
        return pd.DataFrame(cluster_data)
