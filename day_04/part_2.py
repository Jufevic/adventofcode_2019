from collections import defaultdict
from pathlib import Path

from parse import parse

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE_6 = CURRENT_FOLDER / "demo_input_6.txt"
DEMO_INPUT_FILE_7 = CURRENT_FOLDER / "demo_input_7.txt"
DEMO_INPUT_FILE_8 = CURRENT_FOLDER / "demo_input_8.txt"

with open(INPUT_FILE) as f:
    line = f.readline()

first, last = parse("{:d}-{:d}", line)
valid_passwords = 0
for password in range(first, last + 1):
    digits = [int(c) for c in str(password)]
    is_valid = True
    repeat_start = 0
    repeated_digit = digits[0]
    repetitions = defaultdict(lambda: 1)
    for i, (a, b) in enumerate(zip(digits[:-1], digits[1:]), 1):
        if a > b:
            is_valid = False
            break
        if a == b:
            for pos in range(repeat_start, i):
                repetitions[pos] += 1
            repetitions[i] = repetitions[i - 1]
        else:
            repeated_digit = b
            repeat_start = i
    if is_valid and 2 in repetitions.values():
        valid_passwords += 1

print(valid_passwords)
