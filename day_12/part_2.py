from math import lcm
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

x_states = set()
y_states = set()
z_states = set()
x_period = None
y_period = None
z_period = None

step = 0
while any(period is None for period in (x_period, y_period, z_period)):
    stacked = np.stack((positions, velocities))
    # Check if X state was already seen
    if x_period is None:
        x_state = tuple(stacked[:, :, 0].flat)
        if x_state in x_states:
            x_period = step
        x_states.add(x_state)
    # Check if Y state was already seen
    if y_period is None:
        y_state = tuple(stacked[:, :, 1].flat)
        if y_state in y_states:
            y_period = step
        y_states.add(y_state)
    # Check if Z state was already seen
    if z_period is None:
        z_state = tuple(stacked[:, :, 2].flat)
        if z_state in z_states:
            z_period = step
        z_states.add(z_state)
    # Apply gravity
    left = np.tile(positions, (n_rows, 1, 1))
    right = np.transpose(left, axes=(1, 0, 2))
    resulting_force = np.sign(right - left).sum(axis=0)
    velocities += resulting_force

    # Apply velocities
    positions += velocities

    # Move on to the next step
    step += 1

print(lcm(x_period, y_period, z_period))
