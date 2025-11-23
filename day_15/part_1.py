from collections import defaultdict
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DIRECTIONS = {1j: 1, -1j: 2, -1: 3, 1: 4}


start_opcodes = defaultdict(int)
with open(INPUT_FILE) as f:
    for i, element in enumerate(f.readline().split(",")):
        start_opcodes[i] = int(element)


class Program:
    def __init__(self, opcodes, inputs=None):
        """Initialize a program

        :param opcodes: program to run
        :param inputs: arguments to give to the program, must be iterable
        """
        self.opcodes = opcodes
        if inputs is None:
            inputs = []
        self.inputs = iter(inputs)
        self.index = 0
        self.relative_base = 0

    def provide_inputs(self, inputs):
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


grid = {0: -2}
position = 0
distance = 0
distances = {position: distance}
# Arbitrarily start heading north
direction = 1j
start_code = DIRECTIONS[direction]
program = Program(start_opcodes, inputs=[start_code])
for i, status in enumerate(program.run()):
    new_position = position + direction
    # Robot hits a wall
    if status == 0:
        grid[new_position] = 1
        direction *= 1j
    # Robot moved one step in the required position
    elif status == 1:
        if new_position in distances:
            distance = distances[new_position]
        else:
            distance += 1
            distances[new_position] = distance
        grid[new_position] = 0
        position = new_position
        direction *= -1j
    # Robot moved one step in the required position and found the oxygen tank
    elif status == 2:
        grid[new_position] = 2
        position = new_position
        distances[position] = distance + 1
        break

    # Move in the chosen direction
    next_code = DIRECTIONS[direction]
    program.provide_inputs([next_code])

# Plot the results
rows = np.imag(list(grid)).astype(int)
cols = np.real(list(grid)).astype(int)
min_row = rows.min()
max_row = rows.max()
min_col = cols.min()
max_col = cols.max()
n_rows = max_row - min_row + 1
n_cols = max_col - min_col + 1
# Represent the starting tile with -2, unknown tiles with -1, empty tile with 0,
# walls with 1 and the oxysgen tank with 2.
to_plot = np.full((n_rows, n_cols), -1)
for row, col in zip(rows, cols):
    to_plot[row - min_row, col - min_col] = grid[col + 1j * row]

plt.imshow(to_plot)
plt.axis("equal")
plt.axis("off")
plt.show()

print(distances[position])
