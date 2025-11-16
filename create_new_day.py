import os
import shutil
from pathlib import Path

from aocd import get_data

DAY = 11
YEAR = 2019

root_dir = Path(__file__).parent
day_dir = root_dir / f"day_{DAY:02}"
if not os.path.exists(day_dir):
    os.makedirs(day_dir)
    with open(Path(day_dir / "input.txt"), "w") as f:
        f.write(get_data(day=DAY, year=YEAR))
    Path(day_dir / "demo_input.txt").touch()

    shutil.copyfile(root_dir / "template.py", day_dir / "part_1.py")
    Path(day_dir / "part_2.py").touch()

    with open(root_dir / "README.md", "a") as file:
        file.write(f"\n* [day {DAY:02}](day_{DAY:02})")
