def box_area(box: tuple[float, float, float, float]) -> float:
    left, top, right, bottom = box
    return max(0.0, right - left) * max(0.0, bottom - top)


def iou(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    left = max(a[0], b[0])
    top = max(a[1], b[1])
    right = min(a[2], b[2])
    bottom = min(a[3], b[3])
    intersection = box_area((left, top, right, bottom))
    union = box_area(a) + box_area(b) - intersection
    if union <= 0:
        return 0.0
    return intersection / union


if __name__ == "__main__":
    value = iou((0, 0, 2, 2), (1, 1, 3, 3))
    print(f"{value:.6f}")
    assert abs(value - (1 / 7)) < 1e-9
    assert iou((0, 0, 2, 2), (0, 0, 2, 2)) == 1.0