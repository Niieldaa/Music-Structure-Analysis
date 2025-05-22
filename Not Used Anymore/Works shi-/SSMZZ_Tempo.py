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

# Load the audio file
file_path = r"C:\Users\nicol\Pictures\Everything University\2. År\P4 - Lyd Behandling\Semesterprojekt\Emmanual\EXPORT\EXPORT\Audio Files\37. Vitalic - No More Sleep.flac"
y, sr = librosa.load(file_path, sr=None)

# Compute onset envelope (captures energy bursts, rhythmically relevant)
hop_length = 512
onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

# Compute tempogram (time vs tempo)
tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=hop_length)

# Optional downsampling
tempogram_downsampled = tempogram[:, ::1]  # Adjust ::N to reduce resolution if needed

# Compute self-similarity matrix using cosine similarity
similarity_matrix = 1 - cdist(tempogram_downsampled.T, tempogram_downsampled.T, metric='cosine')

# Trim for display (optional)
max_frames = 200
similarity_matrix = similarity_matrix[:max_frames, :max_frames]

# Plot the self-similarity matrix
plt.figure(figsize=(8, 6))
plt.imshow(similarity_matrix, aspect='auto', origin='lower', cmap='coolwarm')
plt.colorbar(label='Cosine Similarity')
plt.title("Self-Similarity Matrix (SSM) - Tempogram (Tempo)")
plt.xlabel("Frame Index")
plt.ylabel("Frame Index")
plt.tight_layout()
plt.show()
