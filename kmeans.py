import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
import stopwords_heb


def find_K(X):
    scores = []
    K = range(2, 20)
    for k in K:
        kmeans_model = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
        kmeans_model_lables = kmeans_model.fit_predict(X)
        silhouette_avg = silhouette_score(X, kmeans_model_lables)
        sample_silhouettes = silhouette_samples(X, kmeans_model_lables)
        under_avg = 0
        for i in sample_silhouettes:
            if i < silhouette_avg:
                under_avg += 1
        scores.append(under_avg)
    result = 0
    for i in range(0, 18):
        if scores[i] == np.min(scores):
            result = i
    return result


def clusterify(docs):
    vectorizer = TfidfVectorizer(stop_words=stopwords_heb.stopwords)
    X = vectorizer.fit_transform(docs)
    K = find_K(X)
    model = KMeans(n_clusters=K, init='k-means++', max_iter=100, n_init=1).fit(X)
    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(K):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),
        print("\n")
    print("\n")
    print("Prediction")