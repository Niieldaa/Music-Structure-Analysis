import numpy as np
import librosa
import librosa.display
import soundfile as sf
from scipy.spatial.distance import cdist
import time


def chroma_representation(audio_path):
    try:
        print(f"Loading audio file: {audio_path}")
        y, sr = librosa.load(audio_path, sr=None)  # Ensure original sample rate
    except Exception as e:
        print(f"Librosa failed to load FLAC, trying soundfile: {e}")
        y, sr = sf.read(audio_path)  # Alternative FLAC loading
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    print("Chroma representation computed.")
    return chroma

def pairwise_similarity(chroma):
    print("Calculating pairwise similarity...")
    similarity = 1 - cdist(chroma.T, chroma.T, metric='cosine')
    print("Pairwise similarity matrix created.")
    return similarity

def segment_comparison(similarity, segment_length=10):
    print("Comparing segments...")
    num_segments = similarity.shape[0] - segment_length + 1
    segments = [np.atleast_2d(similarity[i:i+segment_length]) for i in range(num_segments)]
    print(f"Generated {len(segments)} segments.")
    return segments

def form_segment_families(segments, threshold=0.8):
    start_time = time.time()
    print("Forming segment families...")
    families = []
    for seg in segments:
        seg = np.atleast_2d(seg)  # Ensure segment is 2D
        added = False
        for family in families:
            family_matrix = np.vstack(family)  # Stack into a 2D array
            if np.mean(cdist(family_matrix, seg, metric='cosine')) < threshold:
                family.append(seg)
                added = True
                break
        if not added:
            families.append([seg])
    print(f"Formed {len(families)} segment families in {time.time() - start_time:.2f} seconds.")
    return families

def rate_segment_families(families):
    start_time = time.time()
    print("Rating segment families...")
    scores = [np.mean([np.mean(seg) for seg in family]) for family in families]
    print(f"Segment families rated in {time.time() - start_time:.2f} seconds.")
    return scores

def greedy_selection(families, scores):
    start_time = time.time()
    print("Selecting best segment family...")
    best_family = families[np.argmax(scores)]
    print(f"Best segment family selected in {time.time() - start_time:.2f} seconds.")
    return best_family

def segment_music(audio_path):
    start_time = time.time()
    print("Starting music segmentation process...")
    chroma = chroma_representation(audio_path)
    similarity = pairwise_similarity(chroma)
    segments = segment_comparison(similarity)
    families = form_segment_families(segments)
    scores = rate_segment_families(families)
    best_family = greedy_selection(families, scores)
    print(f"Music segmentation complete in {time.time() - start_time:.2f} seconds.")
    return best_family


# Example Usage
audio_file = r"C:\Users\nield\Desktop\GitHub\Music-Structure-Analysis\DO NOT TOUCH\Audio Files\Emmanuel\01. Vitalic - Polkamatic.flac"  # Replace with actual FLAC file path
best_segment = segment_music(audio_file)

# Resources:
# 1. Chroma Features: https://librosa.org/doc/main/generated/librosa.feature.chroma_stft.html
# 2. Cosine Similarity: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
# 3. Music Segmentation Concepts: https://www.ee.columbia.edu/~dpwe/pubs/Ellis07-sigtrans.pdf