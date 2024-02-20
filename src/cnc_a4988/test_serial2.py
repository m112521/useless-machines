import serial
import time

# Open grbl serial port
s = serial.Serial('COM3', 115200)

# Wake up grbl
s.write(b"\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize 
s.flushInput()  # Flush startup text in serial input


s.write(str.encode('$X' + '\n'))
s.write(str.encode('$H' + '\n'))
s.write(str.encode('G21' + '\n'))
s.write(str.encode('G90' + '\n'))
s.write(str.encode('M3S500' + '\n'))
s.write(str.encode('G0X5.000Y5.000' + '\n'))
s.write(str.encode('G1X42.7384Y52.0254F400' + '\n'))
s.write(str.encode('M3S0' + '\n'))
s.write(str.encode('G1X100.1235Y100.1235F400' + '\n'))


# for line in f:
#     l = line.strip() # Strip all EOL characters for consistency
#     print ('Sending: ' + l),
#     s.write(str.encode(l + '\n')) # Send g-code block to grbl
    #grbl_out = s.readline().decode() # Wait for grbl response with carriage return
    #print (' : ' + grbl_out.strip())

s.close()    
