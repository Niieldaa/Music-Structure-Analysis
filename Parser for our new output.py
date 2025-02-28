# We need to parse the data to something useful - and make them split the songs :)
import csv

def parse_new_data(data):
    # Prepare a list to hold parsed rows
    parsed_data = []

    reader =  csv.DictReader(data.splitlines())

    for row in reader:
        parsed_data.append({
            "FRAME": int(row['FRAME']),
            "VALUE": float(row['VALUE']),
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
        fieldnames = ["FRAME", "VALUE", "DURATION", "LABEL"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        writer.writerows(parsed_data)

file_path = "Files/eh.csv"

file_data = read_file(file_path)
parsed_result = parse_new_data(file_data)

# Output file path where the parsed data will be saved
output_file_path = "Files/Parsed data/parsed_data_new.csv"  # Replace with desired output file path
# Export the parsed result to a new CSV file
export_to_csv(parsed_result, output_file_path)


# Print parsed result in tabular format
from tabulate import tabulate
headers = ["FRAME", "VALUE", "DURATION", "LABEL"]
table = [list(item.values()) for item in parsed_result]

print(tabulate(table, headers=headers, tablefmt="grid"))  # Alternative: "plain", "pipe", "fancy_grid", etc.

print(f"parsed_result is exported to {output_file_path}")
print("Jeg gider ikke at GitHub skal drille sådan her")

