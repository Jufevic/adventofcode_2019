from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"

with open(INPUT_FILE) as f:
    opcodes = [int(element) for element in f.readline().split(",")]

index = 0
input_value = 1
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
            opcodes[operands[0]] = input_value
            index += 2

        # Output operation
        case 4:
            print(opcodes[operands[0]])
            index += 2
