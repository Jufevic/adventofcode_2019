from pathlib import Path

from parse import parse

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"
DEMO_INPUT_FILE_2 = CURRENT_FOLDER / "demo_input_2.txt"


def visited_cells(line):
    visited = {}
    current = 0
    latency = 0
    for instruction in line.split(","):
        letter, steps = parse("{}{:d}", instruction)
        direction = {"U": 1j, "L": -1, "D": -1j, "R": 1}[letter]
        for step in range(1, steps + 1):
            latency += 1
            if current + direction * step not in visited:
                visited[current + direction * step] = latency
        current += direction * steps
    return visited


with open(INPUT_FILE) as f:
    first_line, second_line = f.read().splitlines()

d1 = visited_cells(first_line)
d2 = visited_cells(second_line)
print(min(d1[key] + d2[key] for key in d1.keys() & d2.keys()))
