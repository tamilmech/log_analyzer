from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import pandas as pd


class DBSCANClustering:
    """
    A class to cluster log messages using DBSCAN algorithm.
    """

    def __init__(self, eps=0.5, min_samples=2, metric='cosine'):
        """
        Initialize the DBSCAN clustering parameters.

        Args:
            eps (float): The maximum distance between two samples for one to be considered as in the neighborhood of the other.
            min_samples (int): The number of samples (or total weight) in a neighborhood for a point to be considered as a core point.
            metric (str): The metric to use when calculating distance between instances.
        """
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric

    def cluster(self, df):
        """
        Cluster log messages using DBSCAN.

        Args:
            df (pd.DataFrame): A DataFrame containing a 'message' column.

        Returns:
            pd.DataFrame: A DataFrame with an additional 'cluster' column indicating the cluster assignment.
        """
        if "message" not in df.columns:
            raise ValueError("The DataFrame must contain a 'message' column.")

        # Use TF-IDF to vectorize log messages
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['message'])

        # Apply DBSCAN clustering
        dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples, metric=self.metric)
        df['cluster'] = dbscan.fit_predict(X)

        return df
