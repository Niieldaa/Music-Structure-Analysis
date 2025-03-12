import os
import pandas as pd
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))

# Set your folder path here
folder_path = os.path.join(script_dir, "QMtestNico")  # CSV folder

# Check if the folder exists
if not os.path.exists(folder_path):
    print(f"The folder '{folder_path}' does not exist. Please check the path.")
else:
    # Initialize an empty list to store the differences for each file
    time_differences = []
    file_names = []
    all_time_diffs = []  # List to store all time differences for CSV export

    # Loop through each CSV file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            # Load the CSV file into a DataFrame
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)

            # Check if 'TIME' column exists
            if 'TIME' in df.columns:
                # Convert the 'TIME' column to datetime format (if necessary)
                df['TIME'] = pd.to_datetime(df['TIME'])

                # Calculate the time difference (in seconds) between consecutive rows
                df['TIME_DIFF'] = df['TIME'].diff().dt.total_seconds()

                # Append the differences and file names
                time_differences.append(df['TIME_DIFF'].dropna())  # Remove NaN for the first value
                file_names.append(file_name)

                # Add the differences to the all_time_diffs list for CSV export
                all_time_diffs.append(df[['TIME', 'TIME_DIFF']].dropna())  # Keep 'TIME' and 'TIME_DIFF' for export

    # Concatenate all the time differences from different files into one DataFrame
    combined_df = pd.concat(all_time_diffs, ignore_index=True)

    # Export the combined time differences to a new CSV file
    output_csv_path = os.path.join(script_dir, 'time_differences.csv')
    combined_df.to_csv(output_csv_path, index=False)

    print(f"Time differences exported to {output_csv_path}")

    # Create a plot to visualize the differences
    plt.figure(figsize=(10, 6))

    # Plot the time differences for each file
    for idx, time_diff in enumerate(time_differences):
        plt.plot(time_diff, label=f'File: {file_names[idx]}')

    # Adding labels and title
    plt.xlabel('Index')
    plt.ylabel('Time Difference (seconds)')
    plt.title('Time Differences between Consecutive Rows in CSV Files')
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
