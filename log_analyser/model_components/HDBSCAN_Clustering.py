from sklearn.feature_extraction.text import TfidfVectorizer
from hdbscan import HDBSCAN
import pandas as pd

# -------------------------------------------------------------------
#                   HDBSCAN Clustering
# -------------------------------------------------------------------

class HDBSCANClustering:
    """
    A class to cluster log messages using the HDBSCAN algorithm.
    """

    def __init__(self, min_cluster_size: int = 2, metric: str = 'euclidean'):
        """
        Initialize the HDBSCAN clustering parameters.

        Args:
            min_cluster_size (int): Minimum size of clusters.
            metric (str): Distance metric to use.

        TODO: Add dynamic adjustment of `min_cluster_size` based on dataset size.
        """
        self.min_cluster_size = min_cluster_size
        self.metric = metric

    def cluster(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cluster log messages using HDBSCAN.

        Args:
            df (pd.DataFrame): A DataFrame containing a 'message' column.

        Returns:
            pd.DataFrame: A DataFrame with aggregated clusters.

        Raises:
            ValueError: If the DataFrame does not contain the required 'message' column.

        FIXME: Currently, the TF-IDF vectorizer does not consider domain-specific keywords or custom stop words.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        # Convert messages to a TF-IDF representation
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['message']).toarray()

        # Apply HDBSCAN clustering
        hdbscan = HDBSCAN(min_cluster_size=self.min_cluster_size, metric=self.metric)
        df['cluster'] = hdbscan.fit_predict(X)

        # Aggregate results by cluster
        hdbscan_df = df.groupby('cluster').agg({
            'timestamp': list,  # Collect timestamps in a list
            'message': list     # Collect messages in a list
        }).reset_index()

        return hdbscan_df
