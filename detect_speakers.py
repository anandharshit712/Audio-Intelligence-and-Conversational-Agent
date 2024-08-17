import librosa
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def detect_speakers(audio_file, max_speakers=10):  # Adjust max_speakers as needed
    y, sr = librosa.load(audio_file)

    # Voice Activity Detection
    vad = librosa.effects.split(y, top_db=20)  # Adjust top_db as needed
    speech_segments = [y[start:end] for start, end in vad]

    # Extract features (MFCCs)
    features = []
    for segment in speech_segments:
        if len(segment) < 2048:  # Ensure segment is long enough
            continue
        mfccs = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=13, n_fft=1024)  # Adjust n_fft as needed
        features.append(np.mean(mfccs, axis=1))

    if not features:
        raise ValueError("No valid speech segments found for feature extraction.")

    # Determine the optimal number of clusters using silhouette score
    best_num_clusters = 2
    best_silhouette_score = -1
    for n_clusters in range(2, max_speakers + 1):
        kmeans = KMeans(n_clusters=n_clusters)
        labels = kmeans.fit_predict(features)
        silhouette_avg = silhouette_score(features, labels)
        if silhouette_avg > best_silhouette_score:
            best_silhouette_score = silhouette_avg
            best_num_clusters = n_clusters

    # Cluster features with the optimal number of clusters
    kmeans = KMeans(n_clusters=best_num_clusters)
    kmeans.fit(features)

    # Return the number of detected speaker clusters
    return best_num_clusters

num_speakers = detect_speakers("isolated_audio.wav")
print("Number of speakers:", num_speakers)