import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
'''
Audio duration (longer audio = more frames)
Hop length (smaller hop = more frames)
Sampling rate (higher rate = more frames)
'''

# Load an audio file
file_path = r"C:\Users\nicol\Pictures\Everything University\2. År\P4 - Lyd Behandling\Semesterprojekt\Emmanual\EXPORT\EXPORT\Audio Files\37. Vitalic - No More Sleep.flac"
y, sr = librosa.load(file_path, sr=None)  # Keep original sampling rate

# Compute Chroma features
hop_length = 512
chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop_length)

# Optionally downsample the chroma features (keep every frame in this example)
chroma_downsampled = chroma[:, ::1]  # Adjust ::N if you want downsampling

# Compute the self-similarity matrix using cosine distance
similarity_matrix = 1 - cdist(chroma_downsampled.T, chroma_downsampled.T, metric='cosine')

# Trim to first N frames for visualization (optional)
max_frames = 200
similarity_matrix = similarity_matrix[:max_frames, :max_frames]

# Plot the self-similarity matrix
plt.figure(figsize=(8, 6))
plt.imshow(similarity_matrix, aspect='auto', origin='lower', cmap='coolwarm')
plt.colorbar(label='Cosine Similarity')
plt.title("Self-Similarity Matrix (SSM) - Chroma")
plt.xlabel("Frame Index")
plt.ylabel("Frame Index")
plt.tight_layout()
plt.show()
