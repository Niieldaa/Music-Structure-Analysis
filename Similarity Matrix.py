# Needs input made by us :)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Generate normalized feature sequence
K = 4
M = 100
r = np.arange(M)

b1 = np.zeros((K, M))
b1[0, :] = r
b1[1, :] = M - r
b2 = np.ones((K, M))

X = np.concatenate((b1, b1, np.roll(b1, 2, axis=0), b2, b1), axis=1)

# Normalize feature sequence (L2 normalization)
X_norm = np.linalg.norm(X, axis=0)
X = X / X_norm
X[:, X_norm < 0.001] = 0  # Threshold normalization

# Compute Self-Similarity Matrix (SSM)
S = np.dot(X.T, X)

# Visualization
cmap = 'gray_r'
fig, ax = plt.subplots(2, 2, gridspec_kw={'width_ratios': [1, 0.05], 'height_ratios': [0.2, 1]}, figsize=(6, 5))

# Plot Feature sequence
cax1 = ax[0, 0].imshow(X, aspect='auto', cmap=cmap)
fig.colorbar(cax1, ax=ax[0, 1])
ax[0, 0].set_xlabel('Time (frames)')
ax[0, 0].set_ylabel('')
ax[0, 0].set_title('Feature sequence')

# Plot Self-Similarity Matrix (SSM)
cax2 = ax[1, 0].imshow(S, aspect='auto', cmap=cmap)
fig.colorbar(cax2, ax=ax[1, 1])
ax[1, 0].set_xlabel('Time (frames)')
ax[1, 0].set_ylabel('Time (frames)')
ax[1, 0].set_title('SSM')

plt.tight_layout()
plt.show()
