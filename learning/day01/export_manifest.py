import csv
import json
from pathlib import Path

ROWS = [
    {"id": 1, "source_id": "srcA", "timestamp": 0.5, "status": "matched", "label": "active"},
    {"id": 2, "source_id": "srcA", "timestamp": 1.0, "status": "no_positive", "label": "none"},
    {"id": 3, "source_id": "srcA", "timestamp": 1.5, "status": "unmatched", "label": "active"},
    {"id": 4, "source_id": "srcA", "timestamp": 2.0, "status": "no_box", "label": "active"},
    {"id": 5, "source_id": "srcB", "timestamp": 0.5, "status": "matched", "label": "passive"},
    {"id": 6, "source_id": "srcB", "timestamp": 1.0, "status": "outside_window", "label": "passive"},
    {"id": 7, "source_id": "srcB", "timestamp": 1.5, "status": "no_generator_result", "label": "unknown"},
    {"id": 8, "source_id": "srcB", "timestamp": 2.0, "status": "no_positive", "label": "none"},
]

TRAINABLE = {"matched", "no_positive"}


def next_run_dir(root: Path) -> Path:
    runs = root / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    version = 1
    while (runs / f"v{version}").exists():
        version += 1
    out = runs / f"v{version}"
    out.mkdir()
    return out


def main() -> None:
    root = Path(__file__).resolve().parent
    out = next_run_dir(root)
    for row in ROWS:
        row["trainable"] = row["status"] in TRAINABLE

    (out / "manifest.json").write_text(json.dumps(ROWS, indent=2))

    with (out / "samples.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROWS[0].keys()))
        writer.writeheader()
        writer.writerows(ROWS)

    trainable_ids = [row["id"] for row in ROWS if row["trainable"]]
    yaml_text = "\n".join(
        [
            f"path: {out.as_posix()}",
            "train: train.txt",
            "val: val.txt",
            "names:",
            "  0: passive",
            "  1: active",
            f"trainable_ids: {trainable_ids}",
            "",
        ]
    )
    (out / "dataset.yaml").write_text(yaml_text)
    print(f"wrote {out}")
    print(f"trainable ids: {trainable_ids}")


if __name__ == "__main__":
    main()