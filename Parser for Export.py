import csv

def parse_new_data(data):
    parsed_data = []

    # Use DictReader to parse the data and they are separated by tab
    reader = csv.DictReader(data.splitlines(), delimiter='\t')

    # Print the column names to check for issues
    print(f"Column names: {reader.fieldnames}")

    # Ensure to clean up any extra spaces around column names - because they are set up very weird.
    reader.fieldnames = [field.strip() for field in reader.fieldnames]


    for row in reader:
        print(f"Row: {row}")
        # Extract only the fields we care about
        try:
            parsed_data.append({
                "CLIP_NAME": str(row["CLIP_NAME"]).strip(),  # Keep clip name as a string
                "DURATION": str(row["DURATION"]).strip(),  # Convert duration to seconds
                "TIMESTAMP": str(row["TIMESTAMP"]).strip(),  # Convert timestamp to seconds
            })
        except KeyError as e:
            print(f"Missing key: {e} in row: {row}")

    return parsed_data


# Function to read the .txt file contents, skipping the first N lines
def read_file(file_path, skip_lines=10):
    with open(file_path, 'r') as file:
        # Skip the first `skip_lines` lines and read the rest of the file
        for _ in range(skip_lines):
            next(file)  # Skip each line
        return file.read()



# Function to export data to a new CSV file
def export_to_csv(parsed_data, output_file_path):
    with open(output_file_path, 'w', newline='') as file:
        fieldnames = ["CLIP_NAME", "DURATION", "TIMESTAMP"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        writer.writerows(parsed_data)
        


# Define the input and output file paths
file_path = "Files/Export.txt"  # Adjust this path based on your file location
output_file_path = "Files/Export Folder/parsed_data.csv"  # Adjust the output file path

# Read the file content and parse the data, skipping the first few lines - dont need them
file_data = read_file(file_path, skip_lines=15)

parsed_result = parse_new_data(file_data)

# Export the parsed result to a new CSV file
export_to_csv(parsed_result, output_file_path)

# Print the parsed result to the console
print("CLIP NAME\tDURATION \tTIMESTAMP")
for item in parsed_result:
    print(f"{item['CLIP_NAME']}\t{item['DURATION']:.3f}\t{item['TIMESTAMP']:.3f}")

print(f"parsed_result is exported to {output_file_path}")
