from math import ceil
from pathlib import Path

import numpy as np

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"
DEMO_INPUT_FILE_2 = CURRENT_FOLDER / "demo_input_2.txt"
DEMO_INPUT_FILE_3 = CURRENT_FOLDER / "demo_input_3.txt"

with open(INPUT_FILE) as f:
    line = np.array([int(i) for i in f.readline()])

n = len(line)
pattern = np.array([0, 1, 0, -1], dtype=int)
p = len(pattern)
matrix = np.zeros((n, n), dtype=int)
for i in range(n):
    repeated = np.repeat(pattern, i + 1)
    tiled = np.tile(repeated, ceil(n / (p * (i + 1) - 1)))
    matrix[i, :] = tiled[1 : n + 1]

for _ in range(100):
    line = np.abs(matrix @ line) % 10
print(line[:8])
