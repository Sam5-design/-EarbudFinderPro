from collections import deque
import cv2
import imutils
import numpy as np
import time

buffer_size = 64

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

# Use laptop webcam on Windows
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Could not open webcam. Try changing 0 to 1.")
    exit()

time.sleep(2)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Could not read from webcam.")
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for color_name, (lower, upper) in colors.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(
            mask.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        cnts = imutils.grab_contours(cnts)

        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)

            if M["m00"] != 0:
                center = (
                    int(M["m10"] / M["m00"]),
                    int(M["m01"] / M["m00"])
                )

                if radius > 10:
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
                        5,
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

            cv2.line(
                frame,
                pts[color_name][i - 1],
                pts[color_name][i],
                draw_colors[color_name],
                2
            )

    cv2.imshow("Color Tracker - Press q to quit", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()