from collections import defaultdict
from itertools import batched
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"

start_opcodes = defaultdict(int)
with open(INPUT_FILE) as f:
    for i, element in enumerate(f.readline().split(",")):
        start_opcodes[i] = int(element)


class Program:
    def __init__(self, opcodes, *inputs):
        """Initialize a program

        :param opcodes: program to run
        :param inputs: arguments to give to the program, must be iterable
        """
        self.opcodes = opcodes
        self.inputs = iter(inputs)
        self.index = 0
        self.relative_base = 0

    def provide_inputs(self, *inputs):
        """Change the inputs the program now has to use

        :param inputs: arguments to give to the program, must be iterable
        """
        self.inputs = iter(inputs)

    def interpret_operands(self, number):
        """Return a list of interpreted operands pointers for the current
        operation. If necessary, modify the list of operands.

        In position mode, interpret values as pointers.
        In immediate mode, don't interpret values.
        In relative mode, interpret values as pointers + relative_base

        :param number: Number of operands to interpret
        """
        current_op = self.opcodes[self.index]
        operands = [
            self.opcodes[i] for i in range(self.index + 1, self.index + 1 + number)
        ]
        for i, mode in enumerate(list(f"{current_op:0{number + 2}d}")[-3::-1]):
            # Position mode parameter
            if mode == "0":
                operands[i] = operands[i]
            # Immediate mode parameter
            if mode == "1":
                operands[i] = self.index + 1 + i
            # Relative mode parameter
            elif mode == "2":
                operands[i] = operands[i] + self.relative_base
        return operands

    def run(self):
        """Run a program, yielding values until it halts

        :yield: output values
        """
        while True:
            current_op = self.opcodes[self.index]

            match current_op % 100:
                # Stop operation
                case 99:
                    break

                # Addition operation
                case 1:
                    operands = self.interpret_operands(3)
                    self.opcodes[operands[2]] = (
                        self.opcodes[operands[0]] + self.opcodes[operands[1]]
                    )
                    self.index += 4

                # Multiplication operation
                case 2:
                    operands = self.interpret_operands(3)
                    self.opcodes[operands[2]] = (
                        self.opcodes[operands[0]] * self.opcodes[operands[1]]
                    )
                    self.index += 4

                # Assignment operation
                case 3:
                    operands = self.interpret_operands(1)
                    self.opcodes[operands[0]] = next(self.inputs)
                    self.index += 2

                # Output operation
                case 4:
                    operands = self.interpret_operands(1)
                    self.index += 2
                    yield self.opcodes[operands[0]]

                # Jump-if-true operation
                case 5:
                    operands = self.interpret_operands(2)
                    if self.opcodes[operands[0]] != 0:
                        self.index = self.opcodes[operands[1]]
                    else:
                        self.index += 3

                # Jump-if-false operation
                case 6:
                    operands = self.interpret_operands(2)
                    if self.opcodes[operands[0]] == 0:
                        self.index = self.opcodes[operands[1]]
                    else:
                        self.index += 3

                # Less-than operation
                case 7:
                    operands = self.interpret_operands(3)
                    if self.opcodes[operands[0]] < self.opcodes[operands[1]]:
                        self.opcodes[operands[2]] = 1
                    else:
                        self.opcodes[operands[2]] = 0
                    self.index += 4

                # Equals operation
                case 8:
                    operands = self.interpret_operands(3)
                    if self.opcodes[operands[0]] == self.opcodes[operands[1]]:
                        self.opcodes[operands[2]] = 1
                    else:
                        self.opcodes[operands[2]] = 0
                    self.index += 4

                # Relative base operation
                case 9:
                    operands = self.interpret_operands(1)
                    self.relative_base += self.opcodes[operands[0]]
                    self.index += 2


program = Program(start_opcodes)
print(sum(1 for x, y, tile_id in batched(program.run(), 3) if tile_id == 2))
