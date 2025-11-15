from pathlib import Path

from parse import parse

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input_1.txt"

ascendants = {}

with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        a, b = parse("{}){}", line)
        ascendants[b] = a


def find_depth(body):
    """Find how indirectly a body orbits around COM"""
    current = body
    depth = 0
    while current != "COM":
        current = ascendants[current]
        depth += 1
    return depth


your_depth = find_depth("YOU")
santa_depth = find_depth("SAN")

# Try first possible common ancestor
depth = min(your_depth, santa_depth)
your_ancestor = ascendants["YOU"]
for _ in range(your_depth - depth):
    your_ancestor = ascendants[your_ancestor]
santa_ancestor = ascendants["SAN"]
for _ in range(santa_depth - depth):
    santa_ancestor = ascendants[santa_ancestor]

# Keep looking for ancestor until a common ancestor is found
while your_ancestor != santa_ancestor:
    your_ancestor = ascendants[your_ancestor]
    santa_ancestor = ascendants[santa_ancestor]
    depth -= 1

print(your_depth - depth + santa_depth - depth)
