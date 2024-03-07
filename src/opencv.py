import cv2 as cv
import numpy as np
from cv2 import aruco

cap = cv.VideoCapture(0)
i = 0

while True:
    ret, frame = cap.read()

    smallFrame =cv.resize(frame, (200, 200))

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1.2, 70, param1=50, param2=54, minRadius=0, maxRadius=0)
    #circles = np.uint16(np.around(circles))

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    #if ids is not None:
        #cv2.line(frame_markers, (int(subcr[0][0]), int(subcr[0][1])), (int(subcr[1][0]), int(subcr[1][1])), color, thickness)

    cv.imshow('video', frame_markers)

    if cv.waitKey(1) & 0xFF==ord('x'):
        cv.imwrite(f'{i}.jpg', frame)
        i += 1

    if cv.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv.destroyAllWindows()