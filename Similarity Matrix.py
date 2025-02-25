# Needs input made by us :)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import libfmp.b
import libfmp.c2
import libfmp.c3
import libfmp.c4
import libfmp.c6

# Generate normalized feature sequence
K = 4
M = 100
r = np.arange(M)
b1 = np.zeros((K, M))
b1[0, :] = r
b1[1, :] = M - r
b2 = np.ones((K, M))
X = np.concatenate((b1, b1, np.roll(b1, 2, axis=0), b2, b1), axis=1)
X = libfmp.c3.normalize_feature_sequence(X, norm='2', threshold=0.001)

# Compute Self-Similarity Matrix (SSM)
S = np.dot(np.transpose(X), X)

# Visualization
cmap = 'gray_r'
fig, ax = plt.subplots(2, 2, gridspec_kw={'width_ratios': [1, 0.05], 'height_ratios': [0.2, 1]}, figsize=(4.5, 5))

libfmp.b.plot_matrix(X, Fs=1, ax=[ax[0,0], ax[0,1]], cmap=cmap,
            xlabel='Time (frames)', ylabel='', title='Feature sequence')
libfmp.b.plot_matrix(S, Fs=1, ax=[ax[1,0], ax[1,1]], cmap=cmap,
            title='SSM', xlabel='Time (frames)', ylabel='Time (frames)', colorbar=True);
plt.tight_layout()

plt.tight_layout()
plt.show()
