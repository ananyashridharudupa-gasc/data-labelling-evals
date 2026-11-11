import json
import random
from collections import defaultdict
from pathlib import Path

SOURCES = [f"src{i:02d}" for i in range(10)]
FRAMES = [f"{source}-f{i:02d}" for source in SOURCES for i in range(4)]


def main() -> None:
    order = list(FRAMES)
    random.Random(42).shuffle(order)
    val = order[:6]
    val_set = set(val)
    leftovers = defaultdict(list)
    for frame in FRAMES:
        source = frame.split("-")[0]
        if source in {item.split("-")[0] for item in val} and frame not in val_set:
            leftovers[source].append(frame)
    report = {"val_frames": val, "leftovers_still_available_to_train": leftovers}
    Path("learning/day04/leaky_frames.json").write_text(json.dumps(report, indent=2))
    print(val)


if __name__ == "__main__":
    main()