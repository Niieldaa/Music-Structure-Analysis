import pandas as pd

# Visuals of detected changes
fig, ax = plt.subplots(figsize=(10, 5))
librosa.display.specshow(tempogram, ax=ax, hop_length=hop_length_tempo, sr=sampling_rate, x_axis="s", y_axis="tempo")
ax.set_title("Segment Change Points")

plt.show()

for b in bkps_times[:-1]:
    ax.axvline(b, ls="--", color="red", lw=2)
    print(f"Change detected at: {b:.2f} seconds")

# === CALCULATES SCORE WITHIN 3s OF GT ====
def gaussian_score_flat_top(time_diff, sigma=0.9, flat_top=0.25):
    abs_diff = abs(time_diff)
    if abs_diff <= flat_top:
        return 100.0
    elif abs_diff >= 3:
        return 0.0
    else:
        adjusted_diff = abs_diff - flat_top
        return 100.0 * math.exp(- (adjusted_diff ** 2) / (2 * sigma ** 2))

# === Load ground truth from CSV ===
ground_truth_path = r"Music-Structure-Analysis\DO NOT TOUCH\GroundTruthData\GroundTruthLeft\parsed_data_1.csv"
gt_times = pd.read_csv(ground_truth_path)['TIMESTAMP'].values  # Extract 'TIMESTAMP' column

# Extract segments and display their timestamps
bkps_time_indexes = (sampling_rate * bkps_times).astype(int).tolist()

# store the segments into an array for later
audio_segments = []

for segment_number, (start, end) in enumerate(rpt.utils.pairwise([0] + bkps_time_indexes), start=1):
    start_time = start / sampling_rate
    end_time = end / sampling_rate
    duration = (end - start) / sampling_rate

    segment_audio = signal[start:end]  # Extract segments
    audio_segments.append(segment_audio)

    print(f"Segment {segment_number}: {start_time:.2f}s - {end_time:.2f}s (Duration: {duration:.2f}s)")
    # display(Audio(data=signal[start:end], rate=sampling_rate))

print("number of segments: {}".format(len(audio_segments)))

# === Scoring ===
scores = []
matched_preds = []

for gt in gt_times:
    if len(bkps_times) == 0:
        scores.append(0.0)
        matched_preds.append(None)
        continue
    closest_pred = min(bkps_times, key=lambda p: abs(p - gt))
    matched_preds.append(closest_pred)
    time_diff = closest_pred - gt
    score = gaussian_score_flat_top(time_diff)
    scores.append(score)

# === Results ===
print("\n--- Evaluation Results ---")
for i, (gt, pred, score) in enumerate(zip(gt_times, matched_preds, scores), 1):
    print(f"{i:02}: GT={gt:.2f}s | Closest Pred={pred:.2f}s | Diff={pred - gt:+.2f}s | Score={score:.2f}")

avg_score = np.mean(scores)
print(f"\nAverage Score: {avg_score:.2f}")