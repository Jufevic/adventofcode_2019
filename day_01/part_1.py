from pathlib import Path

import numpy as np

CURRENT_FOLDER = Path(__file__).absolute().parent
INPUT_FILE = CURRENT_FOLDER / "input.txt"
DEMO_INPUT_FILE = CURRENT_FOLDER / "demo_input.txt"

masses = np.loadtxt(INPUT_FILE, dtype=int)
fuels = masses // 3 - 2
print(np.sum(fuels))
