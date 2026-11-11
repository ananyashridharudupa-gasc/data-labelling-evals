import json
import random
from pathlib import Path

SEED = 42
SOURCES = [f"src{i:02d}" for i in range(10)]
VAL_COUNT = 2


def split_sources(sources: list[str], val_count: int, seed: int) -> dict:
    order = list(sources)
    random.Random(seed).shuffle(order)
    val = sorted(order[:val_count])
    train = sorted(order[val_count:])
    overlap = sorted(set(val) & set(train))
    if overlap:
        raise RuntimeError(f"leak: {overlap}")
    return {"seed": seed, "order": order, "train": train, "val": val}


def main() -> None:
    result = split_sources(SOURCES, VAL_COUNT, SEED)
    out = Path("learning/day04")
    out.mkdir(parents=True, exist_ok=True)
    (out / "split.json").write_text(json.dumps(result, indent=2))
    print("val", result["val"])


if __name__ == "__main__":
    main()