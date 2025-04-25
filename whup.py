import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load a sample audio file (Nutcracker, short clip)
y, sr = librosa.load(librosa.example('nutcracker'), duration=10)

# Compute the chromagram using STFT
chroma = librosa.feature.chroma_stft(y=y, sr=sr)

# Normalize chroma vectors to unit norm for cosine similarity
chroma_norm = librosa.util.normalize(chroma, axis=0)

# Compute self-similarity matrix (cosine similarity)
ssm = np.dot(chroma_norm.T, chroma_norm)

# Plot the chromagram
plt.figure(figsize=(10, 4))
librosa.display.specshow(chroma, x_axis='time', y_axis='chroma', cmap='coolwarm')
plt.colorbar(label='Intensity')
plt.title('Chromagram (STFT-based)')
plt.tight_layout()
plt.show()

# Plot the self-similarity matrix (SSM)
plt.figure(figsize=(8, 8))
plt.imshow(ssm, origin='lower', cmap='magma', interpolation='nearest')
plt.title('Self-Similarity Matrix (SSM)')
plt.xlabel('Time Frame')
plt.ylabel('Time Frame')
plt.colorbar(label='Cosine Similarity')
plt.tight_layout()
plt.show()

