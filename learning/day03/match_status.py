import csv
from pathlib import Path
from iou import iou

CASES = [
    {"id": "a", "existing": (0, 0, 2, 2), "generated": (0, 0, 2, 2), "nobody": False},
    {"id": "b", "existing": (0, 0, 2, 2), "generated": (1, 1, 3, 3), "nobody": False},
    {"id": "c", "existing": (0, 0, 2, 2), "generated": None, "nobody": True},
]
THRESHOLD = 0.5


def get_status(case: dict) -> tuple[str, float | None]:
    if case["nobody"]:
        return "no_positive", None
    score = iou(case["existing"], case["generated"])
    if score >= THRESHOLD:
        return "matched", score
    return "unmatched", score


def main() -> None:
    rows = []
    for case in CASES:
        status, score = get_status(case)
        trainable = status in {"matched", "no_positive"}
        rows.append({
            "id": case["id"],
            "iou": score if score is not None else "",
            "status": status,
            "trainable": trainable,
        })
        print(f"row {case['id']}: status={status}, iou={score}, trainable={trainable}")

    out = Path("learning/day03")
    with (out / "status.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "iou", "status", "trainable"])
        writer.writeheader()
        writer.writerows(rows)
    print("wrote status.csv")


if __name__ == "__main__":
    main()