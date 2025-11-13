from pathlib import Path

import numpy as np

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"

masses = np.loadtxt(INPUT_FILE, dtype=int)
total_fuel = 0
for mass in masses:
    fuel = 0
    mass = mass // 3 - 2
    while mass > 0:
        fuel += mass
        mass = mass // 3 - 2
    total_fuel += fuel
print(total_fuel)
