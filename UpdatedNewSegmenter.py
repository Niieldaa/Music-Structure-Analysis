import numpy as np
import librosa

y, sr = librosa.load(r"DO NOT TOUCH/Audio Files/Emmanuel/01. Vitalic.flac",sr=None)
durationOfSong = librosa.get_duration(y=y, sr=sr)

signal, sr = librosa.load(
    r"DO NOT TOUCH/Audio Files/Emmanuel/01. Vitalic.flac",
    sr = None,                                                                      # <-- CAN BE CHANGED :))
    duration=durationOfSong
)

print(f"Loaded signal with shape: {signal.shape}, Sampling rate: {sr}")


# ===================
# =   Beats         =
# ===================
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
print(f"beats: {beats}")
print(f"tempo: {tempo}")
print(f"number of beats: {len(beats)}")

onsets = librosa.onset.onset_detect(y=y, sr=sr)
print(f"onsets: {onsets}")
print(f"number of onsets: {len(onsets)}")


chroma = librosa.feature.chroma_stft(y=y, sr=sr)
print(f"chroma: {chroma}")
print(f"number of chroma: {len(chroma)}")

mfcc = librosa.feature.mfcc(y=y, sr=sr)
print(f"mfcc: {mfcc}")
print(f"number of mfcc: {len(mfcc)}")
