import os
import csv

# Get the script's directory (relative to project root)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define folder paths
folder1 = os.path.join(script_dir, "DO NOT TOUCH", "GroundTruthData", "GroundTruthLeft")  # CSV1 folder
folder2 = os.path.join(script_dir, "Files", "QM Parsed data", "Left")  # CSV2 folder

# Output file
output_csv = os.path.join(script_dir, "comparison_results.csv")

# Function to compare timestamps and durations
def compare(file1, file2, min_tolerance=0.01, max_tolerance=3.0):
    matches = []

    with open(file1, 'r', newline='') as csv_file1, open(file2, 'r', newline='') as csv_file2:
        reader1 = csv.reader(csv_file1)
        reader2 = csv.reader(csv_file2)

        for row1, row2 in zip(reader1, reader2):
            if len(row1) >= 3 and len(row2) >= 3:  # Ensure both rows have enough columns
                try:
                    time1 = float(row1[2])  # Extract timestamp from CSV1
                    duration1 = float(row1[1])  # Extract duration from CSV1

                    time2 = float(row2[0])  # Extract timestamp from CSV2
                    duration2 = float(row2[2])  # Extract duration from CSV2

                    # Calculate absolute differences
                    time_diff = abs(time1 - time2)
                    duration_diff = abs(duration1 - duration2)

                    # Only keep values where time_diff is between 0.5s and 3s
                    if min_tolerance <= time_diff <= max_tolerance:
                        matches.append([
                            os.path.basename(file1), os.path.basename(file2),
                            time1, duration1, time2, duration2,
                            f"{time_diff:.3f}s", f"{duration_diff:.3f}s"
                        ])
                except ValueError:
                    print(f"Skipping row due to invalid number format: {row1} or {row2}")

    return matches

# Open output CSV file for writing
with open(output_csv, mode="w", newline="") as csv_output:
    writer = csv.writer(csv_output)
    writer.writerow([
        "File1", "File2", "Timestamp1", "Duration1",
        "Timestamp2", "Duration2", "Time Difference", "Duration Difference"
    ])

    # Loop through files 1 to 72
    for i in range(1, 73):
        file1 = os.path.join(folder1, f"parsed_data_{i}.csv")
        file2 = os.path.join(folder2, f"parsed_VitalicQM{i}L.csv")

        if os.path.exists(file1) and os.path.exists(file2):
            print(f"\nComparing parsed_data_{i}.csv with parsed_VitalicQM{i}L.csv...")
            matches = compare(file1, file2)

            if matches:
                writer.writerows(matches)
                print(f"Matching segments found in {file1} and {file2}, saved to CSV.")
            else:
                print(f"No matching segments within 0.5s - 3s found in {file1} and {file2}.")
        else:
            print(f"Skipping comparison: One of the files is missing -> {file1} or {file2}")

print(f"\nComparison results saved to {output_csv}")
