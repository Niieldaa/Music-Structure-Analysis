import matplotlib
matplotlib.use('TkAgg')

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_ground_truth(file_path):
    df = pd.read_csv(file_path)
    df = df.sort_values(by='TIMESTAMP').reset_index(drop=True)
    return df

def segment_music(audio_path, gt_path, hop_length=512, sr=22050, plot=True):
    y, sr = librosa.load(audio_path, sr=sr)
    total_duration = librosa.get_duration(y=y, sr=sr)

    # Extract chroma and recurrence (SSM)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)
    chroma = librosa.util.normalize(chroma, axis=1)
    S = librosa.segment.recurrence_matrix(chroma, mode='affinity', sym=True)

    # Get the number of frames and convert to time axis
    n_frames = S.shape[0]
    times = librosa.frames_to_time(np.arange(n_frames), sr=sr, hop_length=hop_length)

    if plot:
        gt = load_ground_truth(gt_path)

        # two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [10, 1]}, sharex=True)

        # Plots ssm
        librosa.display.specshow(S, x_axis='time', y_axis='time', sr=sr, hop_length=hop_length, cmap='jet', ax=ax1)
        ax1.set_title('Chroma Self-Similarity Matrix (SSM) with Ground Truth Annotations')

        # lines to mark GT
        for t in gt['TIMESTAMP']:
            ax1.axvline(x=t, color='cyan', linestyle='--', linewidth=1)
            ax1.axhline(y=t, color='cyan', linestyle='--', linewidth=1)

        # Timeline bar plot (also in seconds)
        for i, row in gt.iterrows():
            start = row['TIMESTAMP']
            dur = row['DURATION']
            end = min(start + dur, total_duration)
            ax2.barh(0, width=end - start, left=start, height=0.8, align='center', color=plt.cm.Set3(i % 12))
            ax2.text((start + end) / 2, 0, row['CLIP_NAME'], ha='center', va='center', fontsize=8, rotation=45)

        # Synchronize x-axis limits between the two plots
        ax2.set_xlim(0, total_duration)  # Ensure x-limits match the total duration of the audio
        ax2.set_yticks([])  # Hide y-axis ticks for the timeline
        ax2.set_xlabel('Time (s)')
        ax2.set_title('Clip Segments (in Seconds)')
        ax2.spines['top'].set_visible(False)  # Hide top and right spines for cleaner layout
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_visible(False)

        # Make sure both subplots share the same x-axis limits
        ax1.set_xlim(0, total_duration)

        # Adjust layout to prevent overlap and make everything fit
        plt.tight_layout()

        # Show the plot
        plt.show()

        # Wait for the user to close the plot
        input("Press Enter to close plot...")

    return S

# Run the function
if __name__ == "__main__":
    segment_music(
        audio_path=r"",
        gt_path="../DO NOT TOUCH/GroundTruthData/GroundTruthRight/parsed_data_1.csv"
    )
