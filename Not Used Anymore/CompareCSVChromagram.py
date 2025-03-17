import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file (adjust the file path accordingly)
csv_file = r"C:\Users\xxmal\Documents\GitHub\4. Semester\Music-Structure-Analysis\Files\Chroma\Chroma1.csv"
chromagram = pd.read_csv(csv_file, header=None).to_numpy()  # Convert to NumPy array

# Normalize chroma features (optional but recommended)
chromagram = chromagram / np.linalg.norm(chromagram, axis=0, keepdims=True)

# Compute the Self-Similarity Matrix (SSM)
ssm = np.dot(chromagram.T, chromagram)

# Plot the SSM
plt.figure(figsize=(8, 8))
plt.imshow(ssm, cmap="inferno", origin="lower")
plt.colorbar(label="Similarity")
plt.title("Self-Similarity Matrix (SSM)")
plt.xlabel("Time Frame")
plt.ylabel("Time Frame")
plt.show()
