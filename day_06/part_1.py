from collections import defaultdict
from pathlib import Path

from parse import parse

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"

orbits = defaultdict(set)

with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        a, b = parse("{}){}", line)
        orbits[a].add(b)

depth = 0
# counter[depth] = number of bodies that are depth away from COM
counter = {}
frontier = {"COM"}
while frontier:
    counter[depth] = len(frontier)
    frontier = set.union(*(orbits[body] for body in frontier))
    depth += 1

print(sum(n * depth for depth, n in counter.items()))
