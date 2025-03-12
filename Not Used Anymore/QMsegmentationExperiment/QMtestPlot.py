import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the CSV file
df = pd.read_csv("time_differences.csv")

# Count occurrences of each unique time difference
time_diff_counts = df["TIME_DIFF"].value_counts().sort_index()

# Display the most common values and their frequencies
print(time_diff_counts.head(10))  # Print the 10 most common values
print(time_diff_counts.tail(3))  # Print the 10 least common values


# Plot a histogram to check the distribution of time differences
plt.figure(figsize=(10, 5))
sns.histplot(df["TIME_DIFF"], bins=30, kde=True, color="blue", alpha=0.6)
plt.xlabel("Time Difference (seconds)")
plt.ylabel("Frequency")
plt.title("Distribution of Time Differences")
plt.grid(True)
plt.show()

# Check for clustering by visualizing density using a KDE plot
plt.figure(figsize=(10, 5))
sns.kdeplot(df["TIME_DIFF"], fill=True, color="green", alpha=0.5)
plt.xlabel("Time Difference (seconds)")
plt.ylabel("Density")
plt.title("Kernel Density Estimation (KDE) of Time Differences")
plt.grid(True)
plt.show()
