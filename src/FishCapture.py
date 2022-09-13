import csv
import math
import random
import time

import numpy as np
import cv2 as cv

from config.configs import constant


def draw_overlay(frame, cap, ticker1, ticker2):
    width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

    half_width = math.trunc(width / 2)
    start_point = (half_width, 0)
    end_point = (half_width, math.trunc(height))

    frame = cv.line(frame, start_point, end_point, (0, 0, 255), 2)
    cv.putText(frame,
               ticker1,
               (5, math.trunc(height / 2)),
               cv.FONT_HERSHEY_SIMPLEX,
               1,
               (255, 255, 0),
               2,
               cv.LINE_4)

    cv.putText(frame,
               ticker2,
               (half_width + 5, math.trunc(height / 2)),
               cv.FONT_HERSHEY_SIMPLEX,
               1,
               (255, 255, 0),
               2,
               cv.LINE_4)

    return frame


def track_fish(filtered, frame):
    # FindContours supports only CV_8UC1 and 32sC1
    gray = cv.cvtColor(filtered, cv.COLOR_BGR2GRAY)
    contours, _ = cv.findContours(gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv.contourArea(contour)
        if area > 3500:
            m = cv.moments(contour)
            c_x = int(m["m10"] / m["m00"])
            c_y = int(m["m01"] / m["m00"])

            cv.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            cv.circle(frame, (c_x, c_y), 7, (255, 255, 255), -1)

            position = 'X:  ' + str(c_x) + '  Y:  ' + str(c_y)
            cv.putText(frame,
                       position,
                       (50, 50),
                       cv.FONT_HERSHEY_SIMPLEX,
                       1,
                       (0, 255, 255),
                       2,
                       cv.LINE_4)
            cv.putText(frame, "GoldFish", (c_x - 20, c_y - 20),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # cv.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    return frame


def apply_color_mask(hsv_frame):
    lower_orange = np.array([7, 150, 50])
    upper_orange = np.array([15, 255, 255])
    mask = cv.inRange(hsv_frame, lower_orange, upper_orange)
    result = cv.bitwise_and(hsv_frame, hsv_frame, mask=mask)

    return result


def init_video_capture(ticker1, ticker2):
    video_path = constant.paths.video_path

    timeout = time.time() + 10  # 10 s

    cap = cv.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Prep tracking
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        result = apply_color_mask(hsv)

        tracked_frame = track_fish(result, frame)
        frame = draw_overlay(tracked_frame, cap, ticker1, ticker2)

        # Show caps
        cv.imshow('frame', frame)

        if timeout:
            print("Timeout!")

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def init_video_cam_capture():
    cv.namedWindow('video')
    cap = cv.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
        mirror = cv.flip(frame, 1)
        cv.imshow('image', mirror)

        c = cv.waitKey(1)
        if c == 27:
            break

    cap.retrieve()
    cap.release()
    cv.destroyAllWindows()


def pick_random_ticker_symbols():
    with open(constant.paths.csv_path, 'r') as csvfile:
        content = csv.reader(csvfile, delimiter=';')
        chosen_rows = random.choices(list(content), k=2)

        ticker1 = chosen_rows[0][0]
        ticker2 = chosen_rows[1][0]

        return ticker1, ticker2


def init_fish_capture():
    ticker1, ticker2 = pick_random_ticker_symbols()
    # init_video_cam_capture()
    init_video_capture(ticker1, ticker2)
