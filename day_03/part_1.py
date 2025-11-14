from pathlib import Path

from parse import parse

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"
DEMO_INPUT_FILE_2 = CURRENT_FOLDER / "demo_input_2.txt"


def visited_cells(line):
    visited = set()
    current = 0
    for instruction in line.split(","):
        letter, steps = parse("{}{:d}", instruction)
        direction = {"U": 1j, "L": -1, "D": -1j, "R": 1}[letter]
        for step in range(1, steps + 1):
            visited.add(current + direction * step)
        current += direction * steps
    return visited


with open(INPUT_FILE) as f:
    first_line, second_line = f.read().splitlines()

common = visited_cells(first_line) & visited_cells(second_line)
print(min(int(abs(c.real) + abs(c.imag)) for c in common))
