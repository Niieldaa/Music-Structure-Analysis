import csv
import os

# Get the script's directory (relative to project root)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define folder paths
folder1 = os.path.join(script_dir, "DO NOT TOUCH", "GroundTruthData", "GroundTruthRight")  # Folder 1 (GroundTruth)
folder2 = os.path.join(script_dir, "Files", "Segmentino Parsed Data", "Right")  # Folder 2 (Parsed Data)

# Output CSV file to save differences
output_csv = os.path.join(script_dir, "precision_recall_differenceSegmentinoRightVSGT.csv")


# Function to compare timestamps and durations
def compare(file1, file2, min_tolerance=0.0, max_tolerance=1.0):
    TP, FP, FN = 0, 0, 0  # Initialize counters

    with open(file1, 'r', newline='', encoding='utf-8') as csv_file1, open(file2, 'r', newline='',
                                                                           encoding='utf-8') as csv_file2:
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
                        if len(row2) >= 3:
                            try:
                                time2 = float(row2[0].strip())  # Ensure value is clean
                                duration2 = float(row2[2].strip())

                                time_diff = abs(time1 - time2)
                                duration_diff = abs(duration1 - duration2)

                                # If within tolerance, count as TP
                                if min_tolerance <= time_diff <= max_tolerance and min_tolerance <= duration_diff <= max_tolerance:
                                    TP += 1
                                    matched = True
                                    break  # Stop checking other rows for this row1
                            except ValueError:
                                print(f"Skipping invalid number format in file2: {row2}")

                    if not matched:
                        FP += 1  # No match found for row1

                except ValueError:
                    print(f"Skipping invalid number format in file1: {row1}")

        # Count unmatched rows in file2 as false negatives
        FN = len(reader2) - TP

    return TP, FP, FN


# Open output CSV file for writing
with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_output:
    writer = csv.writer(csv_output)
    writer.writerow([
        "Precision (Folder1)", "Recall (Folder1)", "Precision (Folder2)", "Recall (Folder2)",
        "Precision Difference", "Recall Difference"
    ])

    # Loop through files 1 to 72 (assuming both folders have the same number of files)
    for i in range(1, 73):
        file1 = os.path.join(folder1, f"parsed_data_{i}.csv")
        file2 = os.path.join(folder2, f"parsed_VitalicSEGMENTINO{i}R.csv")

        if os.path.exists(file1) and os.path.exists(file2):
            print(f"\nComparing parsed_data_{i}.csv with parsed_VitalicSEGMENTINO{i}R.csv...")

            # Compare files and get TP, FP, FN for folder1 and folder2
            TP1, FP1, FN1 = compare(file1, file2)
            TP2, FP2, FN2 = compare(file2, file1)

            # Compute precision and recall for folder1
            precision1 = TP1 / (TP1 + FP1) if (TP1 + FP1) > 0 else 0
            recall1 = TP1 / (TP1 + FN1) if (TP1 + FN1) > 0 else 0

            # Compute precision and recall for folder2
            precision2 = TP2 / (TP2 + FP2) if (TP2 + FP2) > 0 else 0
            recall2 = TP2 / (TP2 + FN2) if (TP2 + FN2) > 0 else 0

            # Calculate difference between folder1 and folder2
            precision_diff = precision1 - precision2
            recall_diff = recall1 - recall2

            # Print results immediately after each file
            print(
                f"Precision (Folder1)={precision1:.4f}, Recall (Folder1)={recall1:.4f}, "
                f"Precision (Folder2)={precision2:.4f}, Recall (Folder2)={recall2:.4f}, "
                f"Precision Difference={precision_diff:.4f}, Recall Difference={recall_diff:.4f}")

            # Write to CSV
            writer.writerow([f"{precision1:.4f}", f"{recall1:.4f}", f"{precision2:.4f}", f"{recall2:.4f}",
                             f"{precision_diff:.4f}", f"{recall_diff:.4f}"])

print(f"\nComparison results saved to {output_csv}")
