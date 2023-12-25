# Useless Machines WP

TBD:
- [x] Gh collision simulation
- [x] Gh non-planar -> Gcode
- [ ] Gh C# plugin -> GRBL
- [x] RPi Pyserial to GRBL  
- [x] Modular linear axes (MLA)
- [x] MLA XY+ assembly
- [x] TCP to point2D using OpenCV
- [ ] Gh Machine Generator
- [ ] Gh SyncSim WS
- [ ] Basement, camera holder and enclosings for electronics
- [ ] Doc Git
- [ ] Web/PDF WP


![MLA](imgs/MLA.jpg)

![CNC](imgs/cnc-shield.jpg)

![Simulation](imgs/gh-sim.gif)


PySerial to GRBL:

```python
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


s.close()    

```
