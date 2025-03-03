import csv
import os

# Get the script's directory (relative to project root)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define folder paths relative to the script
folder1 = os.path.join(script_dir, "Files", "Vitallic")
folder2 = os.path.join(script_dir, "Files", "Parsed data")

# Function to compare two CSV files
def compare(file1, file2):
    differences = []

    # Open both CSV files in read mode
    with open(file1, 'r', newline='') as csv_file1, open(file2, 'r', newline='') as csv_file2:
        reader1 = csv.reader(csv_file1)
        reader2 = csv.reader(csv_file2)

        # Iterate over rows in both files simultaneously
        for row1, row2 in zip(reader1, reader2):
            if row1 != row2:
                differences.append((row1, row2))

    return differences

# Loop through files 1 to 72
for i in range(1, 73):
    file1 = os.path.join(folder1, f"VitalicSegmented{i}.csv")
    file2 = os.path.join(folder2, f"parsed_VitalicSegmented{i}.csv")

    if os.path.exists(file1) and os.path.exists(file2):  # Ensure both files exist
        print(f"Comparing VitalicSegmented{i}.csv with parsed_VitalicSegmented{i}.csv...")
        differences = compare(file1, file2)

        if differences:
            print(f"Differences found in {file1} and {file2}:")
            for diff in differences:
                print(f" - {diff}")
        else:
            print(f"No differences found in {file1} and {file2}.")
    else:
        print(f"Skipping comparison: One of the files missing -> {file1} or {file2}")
