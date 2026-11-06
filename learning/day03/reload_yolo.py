from pathlib import Path

IMAGE_W = 100
IMAGE_H = 100


def xyxy_to_yolo(box, width, height, class_id):
    left, top, right, bottom = box
    bw = right - left
    bh = bottom - top
    cx = left + bw / 2
    cy = top + bh / 2
    return f"{class_id} {cx / width:.6f} {cy / height:.6f} {bw / width:.6f} {bh / height:.6f}"


def yolo_to_xyxy(line, width, height):
    class_id, cx, cy, bw, bh = line.split()
    cx, cy, bw, bh = (float(v) for v in (cx, cy, bw, bh))
    cx *= width
    cy *= height
    bw *= width
    bh *= height
    left = cx - bw / 2
    top = cy - bh / 2
    return int(class_id), (left, top, left + bw, top + bh)


def main() -> None:
    labels = Path("learning/day03/labels")
    labels.mkdir(exist_ok=True)

    # Row a — box (0,0,2,2), class 1 active
    line_a = xyxy_to_yolo((0, 0, 2, 2), IMAGE_W, IMAGE_H, 1)
    (labels / "a.txt").write_text(line_a + "\n")
    print("a.txt:", line_a)

    # Example box (10,20,50,60)
    line_example = xyxy_to_yolo((10, 20, 50, 60), IMAGE_W, IMAGE_H, 1)
    (labels / "example_100.txt").write_text(line_example + "\n")
    print("example_100.txt:", line_example)

    # Row c — empty file, nobody
    (labels / "c.txt").write_text("")
    print("c.txt: empty")

    # Row b — no file created, not trainable

    # Reload and verify
    _, box_a = yolo_to_xyxy(line_a, IMAGE_W, IMAGE_H)
    print("reloaded a.txt:", box_a)
    assert box_a == (0.0, 0.0, 2.0, 2.0)

    _, box_example = yolo_to_xyxy(line_example, IMAGE_W, IMAGE_H)
    print("reloaded example_100.txt:", box_example)
    assert box_example == (10.0, 20.0, 50.0, 60.0)

    print("all reloads ok")


if __name__ == "__main__":
    main()