from collections import defaultdict, deque
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"
DEMO_INPUT_FILE_2 = CURRENT_FOLDER / "demo_input_2.txt"

start_opcodes = defaultdict(int)
with open(INPUT_FILE) as f:
    for i, element in enumerate(f.readline().split(",")):
        start_opcodes[i] = int(element)


def run_program(opcodes, *inputs, start_index=0, relative_base=0):
    """Run a program with arguments and optionally special initialization
    parameters

    :param opcodes: program to run
    :param inputs: arguments to give to the program, must be a deque
    :param start_index: index where to start the program, defaults to 0
    :param relative_base: relative_base initial value, defaults to 0
    :yield: output values
    """
    if inputs is not None:
        inputs = deque(inputs)
    index = start_index
    relative_base = relative_base
    while True:
        current_op = opcodes[index]

        def interpret_operands(number):
            """If necessary, modify inplace the list of operands.

            In position mode, interpret values as pointers.
            In immediate mode, don't interpret values.
            In relative mode, interpret values as pointers + relative_base

            :param number: Number of operands to interpret
            """
            operands = [opcodes[i] for i in range(index + 1, index + 1 + number)]
            for i, mode in enumerate(list(f"{current_op:0{number + 2}d}")[-3::-1]):
                # Position mode parameter
                if mode == "0":
                    operands[i] = operands[i]
                # Immediate mode parameter
                if mode == "1":
                    operands[i] = index + 1 + i
                # Relative mode parameter
                elif mode == "2":
                    operands[i] = operands[i] + relative_base
            return operands

        match current_op % 100:
            # Stop operation
            case 99:
                break

            # Addition operation
            case 1:
                operands = interpret_operands(3)
                opcodes[operands[2]] = opcodes[operands[0]] + opcodes[operands[1]]
                index += 4

            # Multiplication operation
            case 2:
                operands = interpret_operands(3)
                opcodes[operands[2]] = opcodes[operands[0]] * opcodes[operands[1]]
                index += 4

            # Assignment operation
            case 3:
                operands = interpret_operands(1)
                opcodes[operands[0]] = inputs.popleft()
                index += 2

            # Output operation
            case 4:
                operands = interpret_operands(1)
                index += 2
                yield opcodes[operands[0]]

            # Jump-if-true operation
            case 5:
                operands = interpret_operands(2)
                if opcodes[operands[0]] != 0:
                    index = opcodes[operands[1]]
                else:
                    index += 3

            # Jump-if-false operation
            case 6:
                operands = interpret_operands(2)
                if opcodes[operands[0]] == 0:
                    index = opcodes[operands[1]]
                else:
                    index += 3

            # Less-than operation
            case 7:
                operands = interpret_operands(3)
                if opcodes[operands[0]] < opcodes[operands[1]]:
                    opcodes[operands[2]] = 1
                else:
                    opcodes[operands[2]] = 0
                index += 4

            # Equals operation
            case 8:
                operands = interpret_operands(3)
                if opcodes[operands[0]] == opcodes[operands[1]]:
                    opcodes[operands[2]] = 1
                else:
                    opcodes[operands[2]] = 0
                index += 4

            # Relative base operation
            case 9:
                operands = interpret_operands(1)
                relative_base += opcodes[operands[0]]
                index += 2


for output in run_program(start_opcodes, 1):
    print(output)
