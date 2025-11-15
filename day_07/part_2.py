from collections import deque
from itertools import permutations
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE_3 = CURRENT_FOLDER / "demo_input_3.txt"
DEMO_INPUT_FILE_4 = CURRENT_FOLDER / "demo_input_4.txt"

with open(INPUT_FILE) as f:
    start_opcodes = [int(element) for element in f.readline().split(",")]


def run_program(opcodes, inputs=None, start_index=0):
    index = start_index
    while True:
        current_op = opcodes[index]
        operands = [op for op in opcodes[index + 1 : index + 4]]

        def interpret_operands(number):
            """If necessary, modify inplace the list of operands.

            In position mode, interpret values as pointers.
            In immediate mode, don't interpret values.

            :param number: Number of operands to interpret
            """
            for i, mode in enumerate(list(f"{current_op:0{number + 2}d}")[-3::-1]):
                if mode == "0":
                    operands[i] = opcodes[operands[i]]

        match current_op % 100:
            # Stop operation
            case 99:
                break

            # Addition operation
            case 1:
                interpret_operands(2)
                opcodes[operands[2]] = operands[0] + operands[1]
                index += 4

            # Multiplication operation
            case 2:
                interpret_operands(2)
                opcodes[operands[2]] = operands[0] * operands[1]
                index += 4

            # Assignment operation
            case 3:
                opcodes[operands[0]] = inputs.popleft()
                index += 2

            # Output operation
            case 4:
                interpret_operands(1)
                index += 2
                # Return the output, the program itself and the current index
                return operands[0], opcodes, index

            # Jump-if-true operation
            case 5:
                interpret_operands(2)
                if operands[0] != 0:
                    index = operands[1]
                else:
                    index += 3

            # Jump-if-false operation
            case 6:
                interpret_operands(2)
                if operands[0] == 0:
                    index = operands[1]
                else:
                    index += 3

            # Less-than operation
            case 7:
                interpret_operands(2)
                if operands[0] < operands[1]:
                    opcodes[operands[2]] = 1
                else:
                    opcodes[operands[2]] = 0
                index += 4

            # Equals operation
            case 8:
                interpret_operands(2)
                if operands[0] == operands[1]:
                    opcodes[operands[2]] = 1
                else:
                    opcodes[operands[2]] = 0
                index += 4


def amplifiers_output(phase_settings):
    # Store program inputs
    program_inputs = [deque([phase]) for phase in phase_settings]
    program_inputs[0].append(0)
    # Store program opcodes
    programs = [[op for op in start_opcodes] for _ in range(5)]
    # Store start indices
    indices = [0] * 5
    while True:
        for i, (program, start_index, inputs) in enumerate(
            zip(programs, indices, program_inputs)
        ):
            result = run_program(program, inputs, start_index=start_index)
            # Check if the program stopped
            if result is None:
                break
            output, program, index = result
            # Give the program output as input for the next program
            program_inputs[(i + 1) % 5].append(output)
            # If the program didn't stop, store its state and current index
            programs[i] = program
            indices[i] = index
        else:
            continue
        break
    return output


print(max(amplifiers_output(p) for p in permutations(range(5, 10))))
