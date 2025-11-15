from pathlib import Path

import numpy as np

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"

WIDTH = 25
HEIGHT = 6
with open(INPUT_FILE) as f:
    data = [int(element) for element in f.readline()]

data = np.reshape(data, (-1, HEIGHT, WIDTH))
# Count the number of zeroes in each layer
layer_zero_counts = (data == 0).sum(axis=(1, 2))
# Take the layer with minimum amount of zeroes
layer = data[np.argmin(layer_zero_counts)]
# Multiply the number of ones and the number of twos in this layer
print(np.sum(layer == 1) * np.sum(layer == 2))
