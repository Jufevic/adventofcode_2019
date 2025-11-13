from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"
DEMO_INPUT_FILE_2 = CURRENT_FOLDER / "demo_input_2.txt"
DEMO_INPUT_FILE_3 = CURRENT_FOLDER / "demo_input_3.txt"
DEMO_INPUT_FILE_4 = CURRENT_FOLDER / "demo_input_4.txt"

with open(INPUT_FILE) as f:
    opcodes = [int(element) for element in f.readline().split(",")]

# Restore to the "1202 program alarm" state
opcodes[1] = 12
opcodes[2] = 2

current_index = 0
while True:
    current_op = opcodes[current_index]
    # Stop operation
    if current_op == 99:
        break
    operands = opcodes[current_index + 1 : current_index + 4]
    first_index, second_index, output_index = operands
    first = opcodes[first_index]
    second = opcodes[second_index]
    # Addition operation
    if current_op == 1:
        opcodes[output_index] = first + second
    # Multiplication operation
    if current_op == 2:
        opcodes[output_index] = first * second
    current_index += 4

print(opcodes[0])
