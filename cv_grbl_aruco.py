# 2. Undistort

import cv2
import numpy as np
from cv2 import aruco
import serial
import time
from scipy.spatial import distance

MARKER_SIZE_MM = 30
PX_PER_MM = 1.3
s = serial.Serial('/dev/ttyACM0', 115200)


def translate_convert(pt, origin):
    return (abs(pt[0]-origin[0])/PX_PER_MM, abs(pt[1]-origin[1])/PX_PER_MM)


def home_machine():
    s.write(b"\r\n\r\n")
    time.sleep(2)   # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input
    # home and park aside
    s.write(str.encode('M3S500' + '\n'))
    s.write(str.encode('$X' + '\n'))
    s.write(str.encode('$H' + '\n'))
    s.write(str.encode('G21' + '\n'))
    s.write(str.encode('G90' + '\n')) # G90 - absolute mode; G91 - relative mode
    s.write(str.encode('M3S500' + '\n'))
    s.write(str.encode('G0X0.000Y90.000' + '\n'))
    time.sleep(50)


def get_markers():
    cap = cv2.VideoCapture(0)
    frame_markers = None
    origin_px = None
    point_px = None

    while True:
        ret, frame = cap.read()
        #smallFrame = cv2.resize(frame, (200, 200))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        if len(ids) == 2:
            min_id = min(ids)[0]
            origin_idx = np.where(ids==min_id)[0][0]
            point_idx = np.where(ids!=min_id)[0][0]

            origin_px = (corners[origin_idx][0][0][0], corners[origin_idx][0][0][1])
            point_px = (corners[point_idx][0][0][0], corners[point_idx][0][0][1])

            break
    cap.release()

    cv2.imshow('Markers', frame_markers)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"ORIGIN_PX: {origin_px}\nPOINT_PX: {point_px}")

    return (origin_px, point_px)


def get_markers_static():
    frame = cv2.imread("mu_code/0.jpg")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    origin_px = None
    point_px = None
    if ids is not None:
        min_id = min(ids)[0]
        origin_idx = np.where(ids==min_id)[0][0]
        point_idx = np.where(ids!=min_id)[0][0]

        origin_px = (corners[origin_idx][0][0][0], corners[origin_idx][0][0][1])
        point_px = (corners[point_idx][0][0][0], corners[point_idx][0][0][1])

        print(f"ORIGIN_PX: {origin_px}\nPOINT_PX: {point_px}")

    return (origin_px, point_px)


def move_machine(point_px, origin_px):
    #s.write(str.encode('G0X10.000Y10.000' + '\n'))
    pt_mm_x, pt_mm_y = translate_convert(point_px, origin_px)
    print(pt_mm_x, pt_mm_y)
    s.write(str.encode('M3S500' + '\n'))
    s.write(str.encode(f'G1X{pt_mm_y}Y{pt_mm_x}F400\n'))
    s.write(str.encode('M3S0' + '\n'))


if __name__ == "__main__":
    home_machine()

    origin_px, point_px = get_markers()
    if origin_px is not None:
        move_machine(point_px, origin_px)
    else:
        print("No markers found")

    # close serial
    s.close()
