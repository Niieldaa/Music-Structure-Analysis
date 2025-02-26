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
            "LABEL": row["LABEL"]
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
output_file_path = "Files/parsed_data.csv"  # Replace with desired output file path
# Export the parsed result to a new CSV file
export_to_csv(parsed_result, output_file_path)

# Print the parsed result
print("FRAME\tVALUE\tDURATION\tLABEL")  # Column headers
for item in parsed_result:
    print(f"{item['FRAME']}\t{item['VALUE']}\t{item['DURATION']}\t{item['LABEL']}")

print(f"parsed_result is exported to {output_file_path}")

