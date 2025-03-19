import numpy as np
import pandas as pd
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load CSV file
csv_file = r"C:\Users\nield\Desktop\GitHub\Music-Structure-Analysis\Files\QM Parsed data\Left\parsed_VitalicQM2L.csv"  # Update with actual path
df = pd.read_csv(csv_file)

# Extract time, pitch values, and durations
times = df["TIME"].values
values = df["VALUE"].values  # Assuming these are MIDI pitch classes
durations = df["DURATION"].values

# Sampling rate and hop length (for time mapping)
sr = 22050  # Arbitrary sampling rate
hop_length = 512  # Frame hop length

# Create a chroma matrix
chroma = np.zeros((12, int((times[-1] + durations[-1]) * sr / hop_length)))

# Fill the chroma matrix based on VALUE and TIME
for t, v, d in zip(times, values, durations):
    start_frame = int(t * sr / hop_length)
    end_frame = int((t + d) * sr / hop_length)
    chroma[v % 12, start_frame:end_frame] = 1  # Normalize to 12 pitch classes

# Define pitch class labels
pitch_labels = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Plot the chromagram with improved styling
plt.figure(figsize=(10, 4))
librosa.display.specshow(chroma, y_axis="chroma", x_axis="time", sr=sr, hop_length=hop_length, cmap="jet")
plt.colorbar(label="Intensity")
plt.title("Chromagram")
plt.xlabel("Time (s)")
plt.ylabel("Chroma class")
plt.yticks(ticks=np.arange(12), labels=pitch_labels[::-1])  # Reverse order to match reference
plt.show()
