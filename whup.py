import librosa
import librosa.display
import librosa.feature
import matplotlib.pyplot as plt
import numpy as np

import ruptures as rpt

# Load a sample audio file (Nutcracker, short clip)
y, sr = librosa.load(r"DO NOT TOUCH/Audio Files/Emmanuel/01. Vitalic.flac", sr = 4000)

# Compute the chromagram using STFT
chroma = librosa.feature.chroma_stft(y=y, sr=sr)

# Normalize chroma vectors to unit norm for cosine similarity
chroma_norm = librosa.util.normalize(chroma, axis=0)

# Compute self-similarity matrix (cosine similarity)
ssm = np.dot(chroma_norm.T, chroma_norm)

# Plot the self-similarity matrix (SSM)
plt.figure(figsize=(8, 8))
plt.imshow(ssm, origin='lower', cmap='magma', interpolation='nearest')
plt.title('Self-Similarity Matrix (SSM)')
plt.xlabel('Time Frame')
plt.ylabel('Time Frame')
plt.colorbar(label='Cosine Similarity')
plt.tight_layout()
plt.show()
