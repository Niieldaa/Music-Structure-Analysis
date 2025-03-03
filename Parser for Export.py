import csv

def parse_new_data(data):
    parsed_data = []

    # Use DictReader to parse the data and they are separated by tab
    reader = csv.DictReader(data.splitlines(), delimiter='\t')

    # Ensure to clean up any extra spaces around column names
    reader.fieldnames = [field.strip() for field in reader.fieldnames]

    def time_to_seconds(time_string):
        """Converts a time string like '0:00.877' or '10.877' into total seconds."""
        if time_string is None or time_string.strip() == "":  # Handle None or empty strings
            return 0  # Default to 0 seconds if invalid time string

        time_string = time_string.strip()  # Remove extra spaces

        # Case 1: Time format "minutes:seconds.milliseconds"
        if ':' in time_string:
            try:
                minutes, seconds = time_string.split(":")  # Split into minutes and seconds
                seconds, milliseconds = seconds.split(".")  # Split seconds and milliseconds
                total_seconds = int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
            except ValueError:  # Handle invalid format
                return 0  # Return 0 if format is incorrect or split fails

        # Case 2: Time format "seconds.milliseconds" (no minutes)
        else:
            try:
                seconds, milliseconds = time_string.split(".")  # Split seconds and milliseconds
                total_seconds = int(seconds) + int(milliseconds) / 1000
            except ValueError:  # Handle invalid format
                return 0  # Return 0 if format is incorrect or split fails

        return total_seconds

    for row in reader:
        try:
            timestamp_string = row["TIMESTAMP"]  # Get the timestamp from the row
            timestamp_seconds = time_to_seconds(timestamp_string)  # Convert to total seconds

            # Extract the fields we care about
            parsed_data.append({
                "CLIP_NAME": str(row["CLIP_NAME"]).strip(),
                "DURATION": str(row["DURATION"]).strip(),
                "TIMESTAMP": timestamp_seconds  # Total seconds value
            })
        except KeyError as e:
            print(f"Missing key: {e} in row: {row}")

    return parsed_data


# Function to read the .txt file contents, skipping the first N lines
def read_file(file_path, skip_lines_top=10, skip_lines_bottom=0):
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines at once

        # Skip the first `skip_lines_top` lines
        lines_to_read = lines[skip_lines_top:]

        # Skip the last `skip_lines_bottom` lines
        lines_to_read = lines_to_read[:-skip_lines_bottom] if skip_lines_bottom > 0 else lines_to_read

        return ''.join(lines_to_read)

def export_to_csv(parsed_data, output_file_path):
    # Initialize variables
    file_count = 1
    current_data = []

    def write_data_to_file(data, file_index):
        with open(f'{output_file_path}_{file_index}.csv', 'w', newline='') as file:
            fieldnames = ["CLIP_NAME", "DURATION", "TIMESTAMP"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    for row in parsed_data:
        timestamp = row["TIMESTAMP"]

        # Ensure timestamp is not None
        if timestamp is None:
            timestamp = 0  # Default to 0 if None

        # Check if the timestamp is within the 0-5 seconds range
        if 0 <= timestamp <= 3.9:
            # If current data has entries, write them to a file and reset
            if current_data:
                write_data_to_file(current_data, file_count)
                file_count += 1
                current_data = []  # Reset the current data

        # Add the row to the current data
        current_data.append(row)

    # After loop ends, write any remaining data to a file
    if current_data:
        write_data_to_file(current_data, file_count)


# Define the input and output file paths
file_path = "Files/Export.txt"  # Adjust this path based on your file location
output_file_path = "Files/Export Folder/parsed_data"  # Adjust the output file path

# Read the file content and parse the data, skipping the first few lines - don't need them
file_data = read_file(file_path, skip_lines_top=15, skip_lines_bottom=821)

parsed_result = parse_new_data(file_data)

# Export the parsed result to a new CSV file
export_to_csv(parsed_result, output_file_path)

# Print the parsed result to the console
print("CLIP NAME\tDURATION \tTIMESTAMP")
for row in parsed_result:
    print(f"{row['CLIP_NAME']}\t{row['DURATION']}\t{row['TIMESTAMP']}")

print(f"parsed_result is exported to {output_file_path}")
