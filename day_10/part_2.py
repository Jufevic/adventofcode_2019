from cmath import phase, polar
from collections import defaultdict
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE_4 = CURRENT_FOLDER / "demo_input_4.txt"

asteroids = set()
with open(INPUT_FILE) as f:
    for row, line in enumerate(f.read().splitlines()):
        for col, value in enumerate(line):
            if value == "#":
                asteroids.add(row - 1j * col)

max_visible = 0
max_station = None
for station in asteroids:
    others = asteroids - {station}
    phases = {phase(other - station) for other in others}
    if len(phases) > max_visible:
        max_visible = len(phases)
        max_station = station

# Sort asteroids by (ring, phase)
same_phase = defaultdict(set)
for asteroid in asteroids - {max_station}:
    relative = asteroid - max_station
    r, theta = polar(relative)
    # Put purely negative number on the negative side of the branch cut
    if relative.imag == 0 and relative.real < 0:
        theta = phase(-1 - 0j)
    same_phase[theta].add((r, asteroid))
all_asteroids = []
for theta, v in same_phase.items():
    for ring, (r, asteroid) in enumerate(sorted(v)):
        all_asteroids.append((ring, theta, asteroid))
all_asteroids.sort()
vaporization_order = [asteroid for _, _, asteroid in all_asteroids]
print(int(vaporization_order[199].real) - 100 * int(vaporization_order[199].imag))
