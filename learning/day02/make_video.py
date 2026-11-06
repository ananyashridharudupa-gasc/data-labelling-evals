import cv2
import numpy as np

FPS = 30
SECONDS = 3
WIDTH, HEIGHT = 320, 180
SOURCE_ID = "clip_a"


def main() -> None:
    path = "learning/day02/clip_a.mp4"
    writer = cv2.VideoWriter(
        path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        FPS,
        (WIDTH, HEIGHT),
    )
    if not writer.isOpened():
        raise RuntimeError("VideoWriter did not open. Check the folder exists.")

    for frame_index in range(FPS * SECONDS):
        image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        x = frame_index
        cv2.rectangle(image, (x, 40), (x + 30, 100), (0, 0, 255), -1)
        cv2.putText(
            image,
            f"f={frame_index}",
            (8, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
        )
        writer.write(image)
    writer.release()
    print("wrote", path)


if __name__ == "__main__":
    main()