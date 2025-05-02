import csv
import os

# Paths to the two files
script_dir = os.path.dirname(os.path.abspath(__file__))
ground_truth_file = os.path.join(script_dir, "DO NOT TOUCH", "GroundTruthData", "OurOwnAnnotations", "OurCSVData", "El_Viaje_OurData.csv")

prediction_file = os.path.join (script_dir, "DO NOT TOUCH", "GroundTruthData", "OurOwnAnnotations", "OurCSVData", "El_Viaje_OurSegmenterTempo.csv")

# Output CSV path
output_csv = "Singular_El_Viaje_comparison_output.csv"

# Function to compare timestamps and durations
def compare(file1, file2, min_tolerance=0.0, max_tolerance=1.0):
    TP, FP, FN = 0, 0, 0
    matched_indices = set()

    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        reader1 = list(csv.reader(f1))[1:]  # Skip headers
        reader2 = list(csv.reader(f2))[1:]

        for row1 in reader1:
            if len(row1) < 3:
                continue
            try:
                time1 = float(row1[2].strip())
                duration1 = float(row1[1].strip())
                matched = False

                for j, row2 in enumerate(reader2):
                    if j in matched_indices or len(row2) < 3:
                        continue
                    try:
                        time2 = float(row2[0].strip())
                        duration2 = float(row2[2].strip())

                        if (min_tolerance <= abs(time1 - time2) <= max_tolerance and
                                min_tolerance <= abs(duration1 - duration2) <= max_tolerance):
                            TP += 1
                            matched_indices.add(j)
                            matched = True
                            break
                    except ValueError:
                        continue
                if not matched:
                    FP += 1
            except ValueError:
                continue

        FN = len(reader2) - len(matched_indices)

    return TP, FP, FN

# Run comparison
TP, FP, FN = compare(ground_truth_file, prediction_file)

# Compute metrics
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
TN = 0  # TN is not directly computable in this context without full dataset

# Print results
print(f"\nResults:")
print(f"True Positives: {TP}")
print(f"False Positives: {FP}")
print(f"False Negatives: {FN}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1_score:.4f}")

# Save results to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as out_csv:
    writer = csv.writer(out_csv)
    writer.writerow(["File1", "File2", "TP", "FP", "FN", "Precision", "Recall", "F1 Score"])
    writer.writerow([ground_truth_file, prediction_file, TP, FP, FN, f"{precision:.4f}", f"{recall:.4f}", f"{f1_score:.4f}"])

print(f"\nResults saved to {output_csv}")
