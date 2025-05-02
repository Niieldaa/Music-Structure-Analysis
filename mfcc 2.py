import librosa
import numpy as np
import matplotlib.pyplot as plt

# === Load audio ===
signal, sr = librosa.load(r"DO NOT TOUCH/Audio Files/Emmanuel/01. Vitalic.flac", sr=None)

# Constants for MFCC extraction
N, H = 4096, 2048  # N is the FFT size, H is the hop length

# Extract MFCC
X_MFCC = librosa.feature.mfcc(y=signal, sr=sr, hop_length=H, n_fft=N)

# Select the coefficient range 4 to 14 (indexed 4 through 14 inclusive)
coef = np.arange(0, 12)
X_MFCC_upper = X_MFCC[coef, :]

# Visualization using matplotlib
fig, ax = plt.subplots(3, 2, gridspec_kw={'width_ratios': [1, 0.03],
                                          'height_ratios': [2, 2, 0.5]}, figsize=(9, 5))


# MFCC Visualization for selected coefficients (4 to 14)
cax2 = ax[1, 0].imshow(X_MFCC_upper, aspect='auto', origin='lower', cmap='inferno', interpolation='none')
fig.colorbar(cax2, cax=ax[1, 1])
ax[1, 0].set_title('MFCC (coefficients 4 to 14)')
ax[1, 0].set_ylabel('MFCC Coefficients')
ax[1, 0].set_yticks([0, 5, 10])
ax[1, 0].set_yticklabels(coef[0] + [0, 5, 10])



# Adjust layout and show the plot
plt.tight_layout()
plt.show()

print("Min MFCC value:", np.min(X_MFCC))
print("Max MFCC value:", np.max(X_MFCC))

