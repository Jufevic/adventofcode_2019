from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"

WIDTH = 25
HEIGHT = 6
with open(INPUT_FILE) as f:
    data = [int(element) for element in f.readline()]

data = np.reshape(data, (-1, HEIGHT, WIDTH))
# Get the indices of first non-transparent pixels
indices = np.argmax(data != 2, axis=0)
# Use pixels at those layers in the final image
output = np.take_along_axis(data, indices[None, ...], axis=0)[0]
# Show the image
plt.imshow(output)
plt.axis("equal")
plt.axis("off")
plt.show()
