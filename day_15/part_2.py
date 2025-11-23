from collections import defaultdict
from pathlib import Path

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
        # Stop after a whole map tour
        if new_position == 0:
            break
        grid[new_position] = 0
        position = new_position
        direction *= -1j
    # Robot moved one step in the required position and found the oxygen tank
    elif status == 2:
        grid[new_position] = 2
        position = new_position

    # Move in the chosen direction
    next_code = DIRECTIONS[direction]
    program.provide_inputs([next_code])

oxygen_tank = next(position for position, tile_code in grid.items() if tile_code == 2)
empty = {position for position, tile_code in grid.items() if tile_code in (0, -2)}
time = 0
frontier = {oxygen_tank}
filled = {oxygen_tank}
while frontier:
    new_frontier = set()
    for element in frontier:
        for direction in DIRECTIONS:
            neighbour = element + direction
            if neighbour not in filled and neighbour in empty:
                filled.add(neighbour)
                new_frontier.add(neighbour)
    frontier = new_frontier
    time += 1

print(time - 1)
