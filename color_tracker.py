from collections import deque
import cv2
import numpy as np
import time
import math

buffer_size = 32
alpha = 0.20
min_radius = 15
dead_zone = 3

colors = {
    "green": ((29, 86, 6), (64, 255, 255)),
    "blue": ((90, 50, 50), (130, 255, 255)),
    "red": ((0, 50, 50), (10, 255, 255)),
    "yellow": ((20, 100, 100), (30, 255, 255)),
}

draw_colors = {
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "red": (0, 0, 255),
    "yellow": (0, 255, 255),
}

pts = {color: deque(maxlen=buffer_size) for color in colors}

def open_camera():
    backends = [
        ("DSHOW", cv2.CAP_DSHOW),
        ("MSMF", cv2.CAP_MSMF),
        ("ANY", cv2.CAP_ANY),
    ]

    for name, backend in backends:
        for index in [0, 1, 2]:
            print(f"Trying camera {index} with {name}")

            cap = cv2.VideoCapture(index, backend)
            time.sleep(2)

            if not cap.isOpened():
                cap.release()
                continue

            for _ in range(20):
                ret, frame = cap.read()

            if ret and frame is not None and frame.mean() > 1:
                print(f"Using camera {index} with {name}")
                return cap

            cap.release()

    return None


cap = open_camera()

if cap is None:
    print("No working camera found.")
    exit()

window_name = "Stable Color Tracker - Press q to quit"

kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("No frame")
        break

    frame = cv2.resize(frame, (600, int(frame.shape[0] * 600 / frame.shape[1])))

    blurred = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for color_name, (lower, upper) in colors.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(hsv, lower, upper)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        center = None

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)

            if M["m00"] != 0 and radius > min_radius and area > 500:
                raw_center = (
                    int(M["m10"] / M["m00"]),
                    int(M["m01"] / M["m00"])
                )

                if len(pts[color_name]) > 0 and pts[color_name][0] is not None:
                    old_x, old_y = pts[color_name][0]
                    new_x, new_y = raw_center

                    smooth_x = int(old_x * (1 - alpha) + new_x * alpha)
                    smooth_y = int(old_y * (1 - alpha) + new_y * alpha)

                    if abs(smooth_x - old_x) < dead_zone and abs(smooth_y - old_y) < dead_zone:
                        center = (old_x, old_y)
                    else:
                        center = (smooth_x, smooth_y)
                else:
                    center = raw_center

                cv2.circle(
                    frame,
                    (int(x), int(y)),
                    int(radius),
                    draw_colors[color_name],
                    2
                )

                cv2.circle(
                    frame,
                    center,
                    6,
                    draw_colors[color_name],
                    -1
                )

                cv2.putText(
                    frame,
                    color_name,
                    (int(x), int(y) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    draw_colors[color_name],
                    2
                )

        pts[color_name].appendleft(center)

        for i in range(1, len(pts[color_name])):
            if pts[color_name][i - 1] is None or pts[color_name][i] is None:
                continue

            thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)

            cv2.line(
                frame,
                pts[color_name][i - 1],
                pts[color_name][i],
                draw_colors[color_name],
                thickness
            )

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()