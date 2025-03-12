import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import os
import pandas as pd

# Here is the folder path, for which folder of data you want to use.
folder_path = "Files/QM Parsed data/Left"

# Here it checks if the files in the folder are actually csv files.
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Here it makes an empty list to store the data.
#all_times = []
#all_durations = []

# Here is a for loop that goes through each csv file in the folder.
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(file_path)  # Here it reads each csv file into a DataFrame (just like an Excel file).

        # Here you choose which column you want to plot.
        if 'TIME' in df.columns and 'DURATION' in df.columns:
            times = df['TIME'].dropna().tolist()
            durations = df['DURATION'].dropna().tolist()
            #all_times.extend(df['TIME'].dropna().tolist())  # Here it appends/removes not a number values.
            #all_durations.extend(df['DURATION'].dropna().tolist())

            print(f"Creating bar plot for: {file}")

            # Here it prints each bar's values.
            print(f"Bar Values for {file}:")
            for time, duration in zip(times, durations):
                print(f"Time: {time}, Duration: {duration}")

            # Here it will plot the histogram.
            plt.figure(figsize=(12, 6))
            bar_width = 0.5
            plt.bar(times, durations, color='blue', edgecolor='black', alpha=0.5)
            plt.grid(axis="y", linestyle="--", alpha=0.7)

            #plt.xticks(times, rotation=45)

            # Here are all the labels for the histogram.
            plt.xlabel('Time')
            plt.ylabel('Duration')
            plt.title(f'Bar Plot of TIME vs DURATION for {file}', fontweight='bold')

            # Here it will show the histogram.
            plt.show()

    except Exception as e:
        print(f"Error reading {file}: {e}")
