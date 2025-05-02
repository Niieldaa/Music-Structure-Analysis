import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy.fftpack import dct

# === Parameters ===
num_ceps = 12          # Keep MFCCs 2–13 (index 1–13)
nfilt = 26             # Number of Mel filterbanks
NFFT = 512             # FFT window size
cep_lifter = 22        # Liftering coefficient
pre_emphasis = 0.97
frame_size = 0.025     # in seconds
frame_stride = 0.01    # in seconds

def fig_ax(figsize=(15, 5), dpi=150):
    """Return a (matplotlib) figure and ax objects with given size."""
    return plt.subplots(figsize=figsize, dpi=dpi)

# === Load audio ===
signal, sr = librosa.load(r"DO NOT TOUCH/Audio Files/Emmanuel/01. Vitalic.flac", sr=None)

# === Pre-emphasis ===
emphasized = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])

# === Framing ===
frame_len = int(round(frame_size * sr))
frame_step = int(round(frame_stride * sr))
signal_len = len(emphasized)
num_frames = int(np.ceil(float(np.abs(signal_len - frame_len)) / frame_step)) + 1

pad_len = num_frames * frame_step + frame_len
z = np.zeros((pad_len - signal_len))
pad_signal = np.append(emphasized, z)

indices = np.tile(np.arange(0, frame_len), (num_frames, 1)) + \
          np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_len, 1)).T
frames = pad_signal[indices.astype(np.int32, copy=False)]

# === Windowing ===
frames *= np.hamming(frame_len)

# === Power Spectrum ===
mag_frames = np.absolute(np.fft.rfft(frames, NFFT))
pow_frames = ((1.0 / NFFT) * (mag_frames ** 2))

# === Mel Filterbank ===
def hz_to_mel(hz): return 2595 * np.log10(1 + hz / 700)
def mel_to_hz(mel): return 700 * (10**(mel / 2595) - 1)

low_mel = hz_to_mel(0)
high_mel = hz_to_mel(sr / 2)
mel_points = np.linspace(low_mel, high_mel, nfilt + 2)
hz_points = mel_to_hz(mel_points)
bin = np.floor((NFFT + 1) * hz_points / sr).astype(int)

fbank = np.zeros((nfilt, NFFT // 2 + 1))
for m in range(1, nfilt + 1):
    f_m1, f_m, f_p1 = bin[m - 1], bin[m], bin[m + 1]
    fbank[m - 1, f_m1:f_m] = (np.arange(f_m1, f_m) - f_m1) / (f_m - f_m1)
    fbank[m - 1, f_m:f_p1] = (f_p1 - np.arange(f_m, f_p1)) / (f_p1 - f_m)

filter_banks = np.dot(pow_frames, fbank.T)
filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)
filter_banks = 20 * np.log10(filter_banks)  # Convert to dB

# === MFCC via DCT (Keep 2–13) ===
mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1 : num_ceps + 1]

# === Sinusoidal Liftering ===
(nframes, ncoeff) = mfcc.shape
n = np.arange(ncoeff)
lift = 1 + (cep_lifter / 2) * np.sin(np.pi * n / cep_lifter)
mfcc *= lift

# === Transpose for plotting or segmentation ===
mfcc_T = mfcc.T  # Shape: (12, time_frames)

# === Plot ===
fig, ax = plt.subplots(figsize=(12, 4))
librosa.display.specshow(mfcc_T, sr=sr, hop_length=frame_step, x_axis="s", cmap="jet", ax=ax)
ax.set_yticks(np.arange(num_ceps))
ax.set_yticklabels([f"MFCC {i+2}" for i in range(num_ceps)])  # Because we dropped 0th
ax.set_ylabel("MFCC Coefficients")
ax.set_title("MFCCs (Coefficients 2–13 with Liftering)")
img = librosa.display.specshow(mfcc_T, sr=sr, hop_length=frame_step, x_axis="s", cmap="jet", ax=ax)
plt.colorbar(img, ax=ax, format="%+2.f dB")  # ✅ Pass the mappable object
plt.tight_layout()
plt.show()
