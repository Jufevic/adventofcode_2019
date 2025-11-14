from pathlib import Path

from parse import parse

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"
DEMO_INPUT_FILE_2 = CURRENT_FOLDER / "demo_input_2.txt"
DEMO_INPUT_FILE_3 = CURRENT_FOLDER / "demo_input_3.txt"
DEMO_INPUT_FILE_4 = CURRENT_FOLDER / "demo_input_4.txt"
DEMO_INPUT_FILE_5 = CURRENT_FOLDER / "demo_input_5.txt"

with open(INPUT_FILE) as f:
    line = f.readline()

first, last = parse("{:d}-{:d}", line)
valid_passwords = 0
for password in range(first, last + 1):
    digits = [int(c) for c in str(password)]
    has_double = False
    is_valid = True
    for a, b in zip(digits[:-1], digits[1:]):
        if a > b:
            is_valid = False
            break
        if a == b:
            has_double = True
    if is_valid and has_double:
        valid_passwords += 1

print(valid_passwords)
