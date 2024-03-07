import serial
import time


# Open grbl serial port
s = serial.Serial('/dev/ttyACM0', 115200)


x = 50.0
y = 0.0
print(x, y)

s.write(b"\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

s.write(str.encode('$X' + '\n'))
#s.write(str.encode('$H' + '\n'))
s.write(str.encode('G21' + '\n'))
s.write(str.encode('G90' + '\n')) # G90 - absolute mode; G91 - relative mode


rbl_out = s.readline()
s.write(str.encode('M4S350' + '\n'))
time.sleep(2)
rbl_out = s.readline()
#s.write(str.encode('M3S0' + '\n'))
#rbl_out = s.readline()
#s.write(str.encode(f'G0X{x}Y{y}' + '\n'))
#grbl_out = s.readline()


s.close()