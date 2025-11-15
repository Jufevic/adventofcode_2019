from cmath import phase
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"
DEMO_INPUT_FILE_2 = CURRENT_FOLDER / "demo_input_2.txt"
DEMO_INPUT_FILE_3 = CURRENT_FOLDER / "demo_input_3.txt"
DEMO_INPUT_FILE_4 = CURRENT_FOLDER / "demo_input_4.txt"

asteroids = set()
with open(INPUT_FILE) as f:
    for row, line in enumerate(f.read().splitlines()):
        for col, value in enumerate(line):
            if value == "#":
                asteroids.add(row + 1j * col)

max_visible = 0
for station in asteroids:
    others = asteroids - {station}
    phases = {phase(other - station) for other in others}
    max_visible = max(max_visible, len(phases))

print(max_visible)
