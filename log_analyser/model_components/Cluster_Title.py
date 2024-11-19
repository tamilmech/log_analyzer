from keybert import KeyBERT
import pandas as pd

# -------------------------------------------------------------------
#                   Cluster Title Generator
# -------------------------------------------------------------------

class ClusterTitleGenerator:
    """
    A class to generate titles for clusters using KeyBERT.
    """

    def __init__(self):
        """
        Initialize the ClusterTitleGenerator class by loading the KeyBERT model.
        """
        self.kw_model = KeyBERT()

    def generate_titles(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate titles and counts for each cluster.

        Args:
            df (pd.DataFrame): A DataFrame containing 'cluster' and 'message' columns.

        Returns:
            pd.DataFrame: A DataFrame summarizing cluster IDs, titles, and message counts.

        Raises:
            ValueError: If the DataFrame does not contain the required 'cluster' and 'message' columns.
        """
        # Ensure required columns exist
        if "cluster" not in df.columns or "message" not in df.columns:
            raise ValueError("The DataFrame must contain 'cluster' and 'message' columns.")

        # List to store cluster data
        cluster_data: list[dict[str, str | int]] = []

        # Generate titles and counts for each cluster
        for cluster_id in df['cluster'].unique():
            cluster_messages = df[df['cluster'] == cluster_id]['message']
            combined_text = " ".join(cluster_messages)

            # Generate a title using KeyBERT or default to a placeholder
            if combined_text.strip():  # Skip empty clusters
                key_phrases = self.kw_model.extract_keywords(
                    combined_text, 
                    keyphrase_ngram_range=(1, 2), 
                    stop_words='english'
                )
                cluster_title = ", ".join([phrase[0] for phrase in key_phrases[:3]])  # Top 3 phrases
            else:
                cluster_title = "No meaningful messages in this cluster"

            # Append cluster data
            cluster_data.append({
                "Cluster ID": cluster_id,
                "Title": cluster_title,
                "Message Count": len(cluster_messages)
            })

        # Convert the list of dictionaries to a DataFrame
        return pd.DataFrame(cluster_data)
