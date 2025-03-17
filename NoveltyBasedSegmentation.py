import numpy as np
import os, sys, librosa
from scipy import signal
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec
import IPython.display as ipd
import pandas as pd
from numba import jit

sys.path.append('..')
import libfmp.b
import libfmp.c2
import libfmp.c3
import libfmp.c4

# Annotation
fn_ann = os.path.join('Files', 'QM Parsed data', 'Left', 'parsed_VitalicQM1L.csv')
df = pd.read_csv(fn_ann, sep=',', keep_default_na=False, header=0)
print('CSV columns detected:', df.columns)
expected_columns = ['TIME', 'VALUE', 'DURATION', 'LABEL']
if not all(col in df.columns for col in expected_columns):
    raise ValueError(f'ERROR: Expected columns {expected_columns}, but found {df.columns}.')
start_times = df['TIME'].astype(float)
end_times = df['TIME'].astype(float) + df['DURATION'].astype(float)
labels = df['LABEL']
ann = list(zip(start_times, end_times, labels))
color_ann = None
#ann, color_ann = libfmp.c4.read_structure_annotation(fn_ann, fn_ann_color=fn_ann)

# SM
fn_wav = os.path.join('DO NOT TOUCH', 'Audio Files', 'Emmanuel', '01. Vitalic - Polkamatic.wav')
tempo_rel_set = libfmp.c4.compute_tempo_rel_set(0.66, 1.5, 5)
x, x_duration, X, Fs_X, S, I = libfmp.c4.compute_sm_from_filename(fn_wav,
                                                                  L=81, H=10, L_smooth=1, thresh=1, Fs=None)

# Visualization
ann_frames = libfmp.c4.convert_structure_annotation(ann, Fs=Fs_X)
fig, ax = libfmp.c4.plot_feature_ssm(X, 1, S, 1, ann_frames, x_duration*Fs_X,
            label='Time (frames)', color_ann=color_ann, clim_X=[0,1], clim=[0,1],
            title='Feature rate: %0.0f Hz' % Fs_X)