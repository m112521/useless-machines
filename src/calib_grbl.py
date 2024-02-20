import serial
import time

# Open grbl serial port
s = serial.Serial('/dev/ttyACM0', 115200)

# calc delta betweeen true distance traveld by carrige and target distance
# for example: if target_dist=120mm and true_dist=120mm -> pd = 123/120=1.025 -> coeff = 1-0.025=0.975
coeff_x = 1 - 0.025

x = 50.0 * coeff_x
y = 0.0 * coeff_x
print(x, y)

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
s.write(str.encode(f'G0X{x}Y{y}' + '\n'))
grbl_out = s.readline()
s.close()