import csv
import os


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


def parse_csv_file(file_path):
    parsed_data = []

    # Open and read the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                # Convert DURATION to seconds and keep other values intact
                duration_string = row["DURATION"]  # Get the duration from the row
                duration_seconds = time_to_seconds(duration_string)  # Convert to total seconds

                # Update the DURATION column in the row with the converted value
                row["DURATION"] = duration_seconds

                # Add the row to parsed data (with all values preserved)
                parsed_data.append(row)
            except KeyError as e:
                print(f"Missing key: {e} in row: {row}")

    return parsed_data


def process_folder(input_folder, output_folder):
    # Check if the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process all CSV files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)

            # Parse the file and convert the duration to seconds
            parsed_data = parse_csv_file(file_path)

            # Prepare the output file path
            output_file_path = os.path.join(output_folder, filename)

            # Write the processed data to the output CSV file
            with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
                fieldnames = parsed_data[0].keys()  # Dynamically use the fieldnames from the first row
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(parsed_data)

            print(f"Processed {filename} and saved to {output_file_path}")


# Example usage:
input_folder = "Files/Export Folder/L"  # Path to the folder containing the input CSV files
output_folder = "Files/Export Folder/L2"  # Path to the folder where processed files will be saved

process_folder(input_folder, output_folder)
