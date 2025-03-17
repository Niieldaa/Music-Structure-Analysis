import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# Load an audio file
file_path = "DO NOT TOUCH/Audio Files/Emmanuel/01. Vitalic.flac"  # Example file path
y, sr = librosa.load(file_path, sr=None)  # sr=None keeps the original sampling rate

# Compute feature matrix (e.g., MFCCs)
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)

# Compute the self-similarity matrix (SSM) using cosine similarity
similarity_matrix = 1 - cdist(mfcc.T, mfcc.T, metric='cosine')

# Plot the self-similarity matrix
plt.figure(figsize=(8, 6))
plt.imshow(similarity_matrix, aspect='auto', origin='lower', cmap='coolwarm')
plt.colorbar(label='Cosine Similarity')
plt.title("Self-Similarity Matrix (SSM)")
plt.xlabel("Frame Index")
plt.ylabel("Frame Index")
plt.show()
