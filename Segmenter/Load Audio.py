import os
import time
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Import the files
folder_path = "../DO NOT TOUCH/Audio Files/Emmanuel"
if not os.path.exists(folder_path):
    raise FileNotFoundError(f"Error: Directory '{folder_path}' does not exist.")
flac_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.flac') or f.endswith('.FLAC')])
if not flac_files:
    raise FileNotFoundError("No FLAC files found in the specified directory.")


# Compute Chromagram
def compute_chromagram(y, sr):
    start_time = time.time()

    # Compute chromagram using CQT, or SIFT
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512)

    print(f'Chromagram computed in {(time.time() - start_time):.2f} seconds.')

    # Normalize chromagram
    start_time = time.time()
    chroma_norm = np.linalg.norm(chroma, axis=0, ord=2)

    # Avoid division by zero
    chroma_norm[chroma_norm == 0] = 1

    # Normalize chroma matrix (MPEG-7 style)
    chroma_mpeg7 = chroma / chroma_norm

    print(f'Chromagram normalization done in {(time.time() - start_time):.2f} seconds.')
    return chroma, chroma_mpeg7


# Compute Self-Similarity Matrix (SSM)
def compute_ssm(chroma):
    chroma_norm = chroma / np.linalg.norm(chroma, axis=0, ord=2, keepdims=True)
    return np.dot(chroma_norm.T, chroma_norm)


for flac_file in flac_files:
    flac_path = os.path.join(folder_path, flac_file)
    print(f"Processing file: {flac_path}")

    y, sr = librosa.load(flac_path, sr=None, mono=True)
    print(f"Loaded: {flac_path}, Sample Rate: {sr}")

    # Compute Chromagram
    chroma, chroma_mpeg7 = compute_chromagram(y, sr)

    # Compute SSM
    ssm = compute_ssm(chroma)

    # Visualization
    cmap = 'gray_r'
    fig, ax = plt.subplots(2, 2, gridspec_kw={'width_ratios': [1, 0.05], 'height_ratios': [0.2, 1]}, figsize=(5, 5))

    img1 = ax[0, 0].imshow(chroma, aspect='auto', origin='lower', cmap=cmap)
    ax[0, 0].set_title(f'Feature sequence: {flac_file}')
    ax[0, 0].set_xlabel('Time (frames)')
    ax[0, 0].set_ylabel('Chroma')
    fig.colorbar(img1, ax=ax[0, 1])

    img2 = ax[1, 0].imshow(ssm, aspect='auto', origin='lower', cmap=cmap)
    ax[1, 0].set_title('Self-Similarity Matrix')
    ax[1, 0].set_xlabel('Time (frames)')
    ax[1, 0].set_ylabel('Time (frames)')
    fig.colorbar(img2, ax=ax[1, 1])

    plt.tight_layout()
    plt.show()
