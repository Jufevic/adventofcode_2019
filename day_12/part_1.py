from pathlib import Path

import numpy as np
from parse import parse

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"

with open(INPUT_FILE) as f:
    lines = f.read().splitlines()

# Create the positions array
n_rows = len(lines)
positions = np.zeros((n_rows, 3), dtype=int)
for row, line in enumerate(lines):
    x, y, z = parse("<x={:d}, y={:d}, z={:d}>", line)
    positions[row, :] = x, y, z
# Create the velocities array
velocities = np.zeros_like(positions)

for _ in range(1000):
    # Apply gravity
    left = np.tile(positions, (n_rows, 1, 1))
    right = np.transpose(left, axes=(1, 0, 2))
    resulting_force = np.sign(right - left).sum(axis=0)
    velocities += resulting_force

    # Apply velocities
    positions += velocities

potential_energy = np.abs(positions).sum(axis=1)
kinetic_energy = np.abs(velocities).sum(axis=1)
total_energy = (potential_energy * kinetic_energy).sum()
print(total_energy)
