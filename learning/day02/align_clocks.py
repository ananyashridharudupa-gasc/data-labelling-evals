import csv
from pathlib import Path

import cv2

FPS = 30
OFFSET_SECONDS = 0.2
TIMES = [0.5, 1.0, 1.5]
SOURCE_ID = "clip_a"


def frame_index(timestamp: float, offset: float, fps: int) -> int:
    return int(round((timestamp + offset) * fps))


def main() -> None:
    root = Path("learning/day02")
    video_path = root / "clip_a.mp4"
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"cannot open {video_path}")

    panels = []
    rows = []
    for timestamp in TIMES:
        naive = frame_index(timestamp, 0.0, FPS)
        corrected = frame_index(timestamp, OFFSET_SECONDS, FPS)
        for kind, index in (("naive", naive), ("corrected", corrected)):
            capture.set(cv2.CAP_PROP_POS_FRAMES, index)
            ok, image = capture.read()
            if not ok:
                raise RuntimeError(f"failed to read frame {index}")
            label = f"{kind} t={timestamp} f={index}"
            cv2.putText(image, label, (8, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            panels.append(image)
            rows.append(
                {
                    "source_id": SOURCE_ID,
                    "ann_time": timestamp,
                    "offset_seconds": OFFSET_SECONDS if kind == "corrected" else 0.0,
                    "kind": kind,
                    "frame_index": index,
                }
            )

    capture.release()
    sheet = cv2.hconcat(panels)
    cv2.imwrite(str(root / "contact_sheet.png"), sheet)

    with (root / "time_offset.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print("wrote contact_sheet.png and time_offset.csv")


if __name__ == "__main__":
    main()