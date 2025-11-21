from collections import defaultdict
from math import ceil
from pathlib import Path

from parse import parse
from scipy.optimize import bisect

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"
DEMO_INPUT_FILE_1 = CURRENT_FOLDER / "demo_input_1.txt"
DEMO_INPUT_FILE_2 = CURRENT_FOLDER / "demo_input_2.txt"
DEMO_INPUT_FILE_3 = CURRENT_FOLDER / "demo_input_3.txt"
DEMO_INPUT_FILE_4 = CURRENT_FOLDER / "demo_input_4.txt"

needed_for = defaultdict(set)
reactions = {}

with open(INPUT_FILE) as f:
    for line in f.read().splitlines():
        inputs, output = parse("{} => {}", line)
        output_quantity, output_name = parse("{:d} {}", output)
        ingredients = {}
        for group in inputs.split(", "):
            quantity, chemical = parse("{:d} {}", group)
            ingredients[chemical] = quantity
            needed_for[chemical].add(output_name)
        reactions[output_name] = output_quantity, ingredients


def ore_needed_for(fuel):
    # Fully quantified queue
    queue = {"FUEL": fuel}
    # In construction queue
    partial_queue = defaultdict(int)
    partial_needed_for = defaultdict(set)
    while "ORE" not in queue:
        for item, quantity in queue.items():
            # Propagate needs to ingredients
            output_quantity, ingredients = reactions[item]
            # Produce the smallest multiple of output_quantity that is greater than
            # the required quantity
            n_reactions = ceil(quantity / output_quantity)
            for ingredient, amount in ingredients.items():
                partial_needed_for[ingredient].add(item)
                partial_queue[ingredient] += n_reactions * amount
        # Only transfer ingredient from partial_queue to queue once all outputs that
        # this ingredient is needed for have been considered
        new_queue = {}
        # partial_needed_for dict is modified during iteration
        for item in list(partial_needed_for):
            outputs = partial_needed_for[item]
            if outputs == needed_for[item]:
                del partial_needed_for[item]
                quantity = partial_queue.pop(item)
                new_queue[item] = quantity
        queue = new_queue

    return queue["ORE"] - 1_000_000_000_000


# Use scipy to find the greatest argument that produces a negative result
print(int(bisect(ore_needed_for, 1, 100_000_000)))
