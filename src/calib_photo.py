import cv2 as cv
import os

vid = cv.VideoCapture(0)
width = 0
height = 0

i = 0
os.chdir('imgs/calib')

while True:
	ret, frame = vid.read()
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	cv.imshow('caps', gray)

	width = frame.shape[1]
	height = frame.shape[0]

	if cv.waitKey(1) & 0xFF==ord('x'):
		cv.imwrite(f'{i}.png', frame)
		i += 1

	if cv.waitKey(1) & 0xFF==ord('q'):
		break

vid.release()
cv.destroyAllWindows()