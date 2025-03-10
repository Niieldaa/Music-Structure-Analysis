import csv
import os

import matplotlib
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')  # This is needed for the Confusion Matrix to be visualized as a figure
import seaborn as sns

# Get the script's directory (relative to project root)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define folder paths
folder1 = os.path.join(script_dir, "Files", "Export Folder", "L2")  # CSV1 folder
folder2 = os.path.join(script_dir, "Files", "QM Parsed data", "Left")  # CSV2 folder

# Output CSV file to save differences
output_csv = os.path.join(script_dir, "differences_log L2 and Left.csv")


# Function to compare timestamps and durations and compute F1 score
def compare(file1, file2, min_tolerance=0.0, max_tolerance=1.0):
    TP, FP, FN = 0, 0, 0  # Initialize counters
    differences = []
    matched_indices = set()  # Track matched rows in file2

    with open(file1, 'r', newline='', encoding='utf-8') as csv_file1, open(file2, 'r', newline='', encoding='utf-8') as csv_file2:
        reader1 = list(csv.reader(csv_file1))
        reader2 = list(csv.reader(csv_file2))

        # **Skip headers** (first row)
        reader1 = reader1[1:] if len(reader1) > 1 else []
        reader2 = reader2[1:] if len(reader2) > 1 else []

        for i, row1 in enumerate(reader1):
            matched = False  # Track if the row is matched

            if len(row1) >= 3:
                try:
                    time1 = float(row1[2].strip())  # Ensure value is clean
                    duration1 = float(row1[1].strip())

                    for j, row2 in enumerate(reader2):
                        if j in matched_indices:  # Skip already matched rows
                            continue
                        if len(row2) >= 3:
                            try:
                                time2 = float(row2[0].strip())  # Ensure value is clean
                                duration2 = float(row2[2].strip())

                                time_diff = abs(time1 - time2)
                                duration_diff = abs(duration1 - duration2)

                                # If within tolerance, count as TP
                                if min_tolerance <= time_diff <= max_tolerance and min_tolerance <= duration_diff <= max_tolerance:
                                    TP += 1
                                    matched_indices.add(j)  # Mark row2 as matched
                                    matched = True
                                    break  # Stop checking other rows for this row1
                            except ValueError:
                                print(f"Skipping invalid number format in file2: {row2}")

                    if not matched:
                        FP += 1  # No match found for row1

                except ValueError:
                    print(f"Skipping invalid number format in file1: {row1}")

        # Count unmatched rows in file2 as false negatives
        FN = len(reader2) - len(matched_indices)

    return TP, FP, FN



# Open output CSV file for writing
with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_output:
    writer = csv.writer(csv_output)
    writer.writerow([
        "File1", "File2", "True Positives", "False Positives", "False Negatives",
        "Precision", "Recall", "F1 Score"
    ])

    total_TP, total_FP, total_FN = 0, 0, 0  # Track totals for all files

    # Loop through files 1 to 72
    for i in range(1, 73):
        file1 = os.path.join(folder1, f"parsed_data_{i}.csv")
        file2 = os.path.join(folder2, f"parsed_VitalicSegmented{i}L.csv")

        if os.path.exists(file1) and os.path.exists(file2):
            print(f"\nComparing parsed_data_{i}.csv with parsed_VitalicSegmented{i}L.csv...")
            TP, FP, FN = compare(file1, file2)

            # Compute precision, recall, and F1 score
            precision = TP / (TP + FP) if (TP + FP) > 0 else 0
            recall = TP / (TP + FN) if (TP + FN) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            # Print results immediately after each file
            print(
                f"→ File {i}: TP={TP}, FP={FP}, FN={FN}, Precision={precision:.4f}, Recall={recall:.4f}, F1 Score={f1_score:.4f}")

            # Write to CSV
            writer.writerow([file1, file2, TP, FP, FN, f"{precision:.4f}", f"{recall:.4f}", f"{f1_score:.4f}"])

            # Update totals
            total_TP += TP
            total_FP += FP
            total_FN += FN

        else:
            print(f"Skipping comparison: One of the files is missing -> {file1} or {file2}")

# Compute overall F1 score
overall_precision = total_TP / (total_TP + total_FP) if (total_TP + total_FP) > 0 else 0
overall_recall = total_TP / (total_TP + total_FN) if (total_TP + total_FN) > 0 else 0
overall_f1_score = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

# Estimate Total Comparisons
total_comparisons = total_TP + total_FP + total_FN  # Total elements considered

# Compute True Negatives (TN)
total_TN = max(0, total_comparisons - (total_TP + total_FP + total_FN))

# All print statements for precision, recall, f1-score and TN
print("\nOverall F1 Score Results:")
print(f"Precision: {overall_precision:.4f}")
print(f"Recall: {overall_recall:.4f}")
print(f"F1 Score: {overall_f1_score:.4f}")
print(f"True Negatives (TN): {total_TN}")  # Print TN

# Create Confusion Matrix in text/console format
conf_matrix = np.array([[total_TP, total_FN], [total_FP, total_TN]])

# Print Confusion Matrix in Console
print("\nConfusion Matrix:")
print(f"                 Predicted Positive   Predicted Negative")
print(f"Actual Positive    {total_TP:<18}     {total_FN:<18}")
print(f"Actual Negative    {total_FP:<18}     {total_TN:<18}")

# Plot Confusion Matrix as a figure
plt.figure(figsize=(5, 4))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Predicted Positive", "Predicted Negative"],
            yticklabels=["Actual Positive", "Actual Negative"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Append overall F1 score to CSV
with open(output_csv, mode="a", newline="", encoding="utf-8") as csv_output:
    writer = csv.writer(csv_output)
    writer.writerow(["Overall", "", total_TP, total_FP, total_FN, total_TN, f"{overall_precision:.4f}", f"{overall_recall:.4f}", f"{overall_f1_score:.4f}"])

print(f"\nComparison results saved to {output_csv}")