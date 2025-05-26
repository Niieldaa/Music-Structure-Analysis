import csv
import os

def parse_new_data(data):
    parsed_data = []
    reader = csv.DictReader(data.splitlines())

    for row in reader:
        parsed_data.append({
            "TIME": round(float(row['TIME']), 1),
            "VALUE": int(row['VALUE']),
            "DURATION": round(float(row['DURATION']), 1),
            "LABEL": str(row["LABEL"])
        })
    return parsed_data

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def export_to_csv(parsed_data, output_file_path):
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)  # Ensure the directory exists
    with open(output_file_path, 'w', newline='') as file:
        fieldnames = ["TIME", "VALUE", "DURATION", "LABEL"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_data)
    print(f"Exported: {output_file_path}")

def process_files_in_folder(folder_path, output_folder):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    for file_name in all_files:
        file_path = os.path.join(folder_path, file_name)

        file_data = read_file(file_path)
        parsed_result = parse_new_data(file_data)

        output_file_name = f"parsed_{file_name}"
        output_file_path = os.path.join(output_folder, output_file_name)

        export_to_csv(parsed_result, output_file_path)

        print(f"Processed and saved: {output_file_path}")

# Use absolute paths for safety
file_folder = r'C:\Users\anbom\Documents\GitHub\Music-Structure-Analysis\Ruptures_segmented_audio_csv'
output_folder = r'C:\Users\anbom\Documents\GitHub\Music-Structure-Analysis\Ruptures_parsed_data'

process_files_in_folder(file_folder, output_folder)
