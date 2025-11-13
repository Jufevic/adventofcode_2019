from copy import deepcopy
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"

with open(INPUT_FILE) as f:
    initial_opcodes = [int(element) for element in f.readline().split(",")]


def program_output(noun, verb, opcodes):
    opcodes[1] = noun
    opcodes[2] = verb
    current_index = 0
    while True:
        opcode = opcodes[current_index]
        # Stop operation
        if opcode == 99:
            break
        parameters = opcodes[current_index + 1 : current_index + 4]
        first_index, second_index, output_index = parameters
        first = opcodes[first_index]
        second = opcodes[second_index]
        # Addition operation
        if opcode == 1:
            opcodes[output_index] = first + second
        # Multiplication operation
        if opcode == 2:
            opcodes[output_index] = first * second
        current_index += 4
    return opcodes[0]


for noun in range(100):
    for verb in range(100):
        try:
            output = program_output(noun, verb, deepcopy(initial_opcodes))
        except IndexError:
            pass
        # print(noun, verb, output)
        if output == 19690720:
            print(100 * noun + verb)
            break
    else:
        continue
    break
