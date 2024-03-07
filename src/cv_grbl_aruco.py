# 2. Undistort
import cv2
import numpy as np
from cv2 import aruco
import serial
import time
from scipy.spatial import distance


MARKER_SIZE_MM = 30
#PX_PER_MM = 1.3
s = serial.Serial('/dev/ttyACM0', 115200)


def load_camera_mtx():
    cameraMatrix = np.load('mu_code/params/cameraMatrix.npy')
    dist = np.load('mu_code/params/dist.npy')

    return cameraMatrix, dist


def undistort_img(img, cameraMatrix, dist):
    h,  w = img.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

    # No remapping
    undist_img = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # Undistort with Remapping
    #mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
    #undist_img_re = cv2.remap(img, mapx, mapy, cv.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    #undist_img = undist_img[y:y+h, x:x+w]

    return undist_img


def calc_px_per_mm(pt_bl, pt_tl, marker_size_mm):
    return distance.euclidean(pt_bl, pt_tl) / marker_size_mm


def translate_convert(pt, origin, px_per_mm):
    return (abs(pt[0]-origin[0])/px_per_mm, abs(pt[1]-origin[1])/px_per_mm)


def translate_convert_mm(pt, origin, px_per_mm):
    # swap X and Y because CNC_XY is fliped relative to OpenCV_XY
    return (abs(pt[1]-origin[1])/px_per_mm-5, abs(pt[0]-origin[0])/px_per_mm+5)


def get_machine_position():
    s.write(str.encode('?'))
    return s.readline().strip().decode('utf-8')


def home_machine():
    s.write(b"\r\n\r\n")
    time.sleep(2)   # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input
    # home and park aside
    #s.write(str.encode('M3S500' + '\n'))
    s.write(str.encode('$X' + '\n'))
    s.write(str.encode('$H' + '\n'))
    s.write(str.encode('G21' + '\n'))
    s.write(str.encode('G90' + '\n')) # G90 - absolute mode; G91 - relative mode
    s.write(str.encode('M3S500' + '\n'))
    rbl_out = s.readline()
    s.write(str.encode('G0X0.000Y90.000' + '\n'))
    grbl_out = s.readline()

    s.write(str.encode('?'))
    print(s.readline().strip().decode('utf-8'))

    time.sleep(30)


def get_all_markers(origin_px, px_per_mm, cameraMatrix, dist, origin_px_u):
    cap = cv2.VideoCapture(0)
    points = []

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # raw image
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        # undistorted image
        frame_u = undistort_img(frame, cameraMatrix, dist)
        gray_u = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners_u, ids_u, _ = aruco.detectMarkers(gray_u, aruco_dict, parameters=parameters)
        frame_markers_u = aruco.drawDetectedMarkers(frame_u.copy(), corners_u, ids_u)

        if (ids is not None):
            for pt in corners:
                point_px = (pt[0][0][0], pt[0][0][1])
                point_mm = translate_convert_mm(point_px, origin_px, px_per_mm)
                points.append(point_mm)
                print(f"RAW:\n{point_px}, {point_mm}")
            for pt_u in corners_u:
                point_px_u = (pt_u[0][0][0], pt_u[0][0][1])
                point_mm_u = translate_convert_mm(point_px_u, origin_px_u, px_per_mm)
                #points.append(point_mm_u)
                print(f"UND:\n{point_px_u}, {point_mm_u}")
            break
        else:
            print(f"Markers not found")
    cap.release()

    cv2.imshow('Markers', frame_markers)
    #compare_img = np.concatenate((frame_markers, frame_markers_u), axis=1)
    #cv2.imshow('Raw vs undistorted', compare_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return points


def get_marker():
    cap = cv2.VideoCapture(0)
    frame_markers = None
    origin_px = None
    origin_px_u = None
    top_right_pt = None

    cameraMatrix, dist = load_camera_mtx()

    # UNDIST IMG -> find markers

    while True:
        ret, frame = cap.read()
        #smallFrame = cv2.resize(frame, (200, 200))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        frame_u = undistort_img(frame, cameraMatrix, dist)
        gray_u = cv2.cvtColor(frame_u, cv2.COLOR_BGR2GRAY)
        corners_u, ids_u, _ = aruco.detectMarkers(gray_u, aruco_dict, parameters=parameters)
        frame_markers_u = aruco.drawDetectedMarkers(frame_u.copy(), corners_u, ids_u)

        if (ids is not None) and min(ids)[0] == 1:
            min_id = min(ids)[0]
            origin_idx = np.where(ids==min_id)[0][0]

            min_id_u = min(ids_u)[0]
            origin_idx_u = np.where(ids_u==min_id_u)[0][0]
            print(corners[origin_idx])

            origin_px = (corners[origin_idx][0][0][0], corners[origin_idx][0][0][1])
            origin_px_u = (corners_u[origin_idx_u][0][0][0], corners_u[origin_idx_u][0][0][1])
            top_right_pt = (corners[origin_idx][0][1][0], corners[origin_idx][0][1][1])

            break
        else:
            print(f"Init marker not found")
    cap.release()

    compare_img = np.concatenate((frame_markers, frame_markers_u), axis=1)
    cv2.imshow('Markers', frame_markers)
    #cv2.imshow("Raw vs Undistorted", compare_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"ORIGIN_PX: {origin_px}")
    return (origin_px, top_right_pt, cameraMatrix, dist, origin_px_u)


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


def draw_x(pt_mm_x, pt_mm_y, size):
    s.write(str.encode('M3S0' + '\n'))
    grbl_out = s.readline()
    s.write(str.encode(f'G1X{pt_mm_x-size}Y{pt_mm_y+size}F200\n'))
    grbl_out = s.readline()

    #s.write(str.encode('?'))
    #print(s.readline().strip().decode('utf-8'))

    s.write(str.encode(f'G1X{pt_mm_x+size}Y{pt_mm_y-size}F200\n'))
    grbl_out = s.readline()

    #s.write(str.encode('?'))
    #print(s.readline().strip().decode('utf-8'))

    s.write(str.encode('M3S500' + '\n'))
    grbl_out = s.readline()
    s.write(str.encode(f'G1X{pt_mm_x-size}Y{pt_mm_y-size}F200\n'))
    grbl_out = s.readline()

    #s.write(str.encode('?'))
    #print(s.readline().strip().decode('utf-8'))

    s.write(str.encode('M3S0' + '\n'))
    grbl_out = s.readline()
    s.write(str.encode(f'G1X{pt_mm_x+size}Y{pt_mm_y+size}F200\n'))
    grbl_out = s.readline()

    #s.write(str.encode('?'))
    #print(s.readline().strip().decode('utf-8'))


def move_machine(point_px, origin_px, px_per_mm):
    pt_mm_y, pt_mm_x = translate_convert(point_px, origin_px, px_per_mm)
    #print(pt_mm_x, pt_mm_y)

    s.write(str.encode('M3S500' + '\n'))
    grbl_out = s.readline()
    s.write(str.encode(f'G1X{pt_mm_x}Y{pt_mm_y}F200\n'))
    grbl_out = s.readline()

    #s.write(str.encode('?'))
    #print(s.readline().strip().decode('utf-8'))

    s.write(str.encode('M3S0' + '\n'))
    grbl_out = s.readline()

    draw_x(pt_mm_x, pt_mm_y, 5)
    #draw_x(pt_mm_x, pt_mm_y, 15)


def move_machine_gh(x, y):
    s.write(str.encode(f'G1X{x}Y{y}F200\n'))
    grbl_out = s.readline()
    #draw_x(x, y, 5)


if __name__ == "__main__":
    home_machine()
    origin_px, top_right_pt, point_px = get_markers()
    if origin_px is not None:
        px_per_mm = calc_px_per_mm(origin_px, top_right_pt, MARKER_SIZE_MM)
        #draw_x(120, 90, 5)
        move_machine(point_px, origin_px, px_per_mm)
    else:
        print("No markers found")

    #input("  Press <Enter> to exit and disable grbl.")

    # close serial
    s.close()