# We need to parse the data to something useful - and make them split the songs :)
import csv
import os


def parse_new_data(data):
    # Prepare a list to hold parsed rows
    parsed_data = []

    reader =  csv.DictReader(data.splitlines())

    for row in reader:
        parsed_data.append({
            "TIME": float(row['TIME']),
            "VALUE": int(row['VALUE']),
            "DURATION": float(row['DURATION']),
            "LABEL": ord(row["LABEL"].upper()) - ord('A') + 1
        })
    return parsed_data

# Function to read CSV file contents
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# Function to export data to a new CSV file
def export_to_csv(parsed_data, output_file_path):
    with open(output_file_path, 'w', newline='') as file:
        fieldnames = ["TIME", "VALUE", "DURATION", "LABEL"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        writer.writerows(parsed_data)

def process_files_in_folder(folder_path, output_folder):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    all_parsed_data = []

    for file_name in all_files:
        file_path = os.path.join(folder_path, file_name)

        file_data = read_file(file_path)
        parsed_result = parse_new_data(file_data)

        all_parsed_data.extend(parsed_result)

        output_file_name = f"parsed_{file_name}"
        output_file_path = os.path.join(output_folder, output_file_name)

        export_to_csv(parsed_result, output_file_path)

        print(f"Processed and exported parsed data for {file_name} to {output_file_path}")

    return all_parsed_data


# located files
file_folder = 'Files/Vitallic/RightSegmented'
output_folder = 'Files/Parsed data/Right'

process_files_in_folder(file_folder, output_folder)

print(f"All parsed data is exported to {output_folder}")

