
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Gaussian tolerance function
def gaussian_score_flat_top(time_diff, sigma=0.9, flat_top=0.25):
    abs_diff = abs(time_diff)
    if abs_diff <= flat_top:
        return 100.0
    elif abs_diff >= 3:
        return 0.0
    else:
        adjusted_diff = abs_diff - flat_top
        return 100.0 * math.exp(- (adjusted_diff ** 2) / (2 * sigma ** 2))

# File paths
GT = r"C:\Users\nicol\Documents\GitHub\Music-Structure-Analysis\DO NOT TOUCH\GroundTruthData\GroundTruthRight\parsed_data_1.csv"
PRED = r"C:\Users\nicol\Documents\GitHub\Music-Structure-Analysis\DO NOT TOUCH\DataProcessing\OurOwnAnnotations\OurCSVData\Polkamatic_OurSegmenterTempo.csv"  # Replace with actual prediction file path


# Load timestamps
gt_times = pd.read_csv(GT)["TIMESTAMP"].dropna().astype(float).values
pred_times = pd.read_csv(PRED)["TIMESTAMP"].dropna().astype(float).values

# Compare timestamps using Gaussian score
TP = 0
matched_pred_indices = set()

for gt_time in gt_times:
    best_score = 0
    best_index = -1
    for i, pred_time in enumerate(pred_times):
        if i in matched_pred_indices:
            continue
        score = gaussian_score_flat_top(pred_time - gt_time)
        if score > 0 and score > best_score:
            best_score = score
            best_index = i
    if best_index >= 0:
        TP += 1
        matched_pred_indices.add(best_index)

FP = len(gt_times) - TP
FN = len(pred_times) - len(matched_pred_indices)

# Metrics
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
accuracy = TP / (TP + FP + FN) if (TP + FP + FN) > 0 else 0

# Output
print(f"\nTrue Positives (within 3s using Gaussian tolerance): {TP}")
print(f"False Positives: {FP}")
print(f"False Negatives: {FN}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"Accuracy: {accuracy:.4f}")
print(f"F1 Score: {f1_score:.4f}")

pd.DataFrame([{
    "True Positives": TP,
    "False Positives": FP,
    "False Negatives": FN,
    "Precision": precision,
    "Recall": recall,
    "Accuracy": accuracy,
    "F1 Score": f1_score
}]).to_csv("OurAnnotationsFMeasure/EmmanuelAnnotationsFMeasure/SingularFMeasure_Emmanuel_PolkamaticTempo.csv", index=False)
