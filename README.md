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


WS stream grbl status:

```python
import serial
import time
from fastapi import FastAPI, Response, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import cv_grbl_aruco as cnc

origins = ["*"]
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

cnc.home_machine()
cnc.draw_x(120, 90, 5)

m_pos = 0
#@app.on_event('startup')
#def init_data():
#    pass

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global m_pose
    global cnc
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            m_pos = cnc.get_machine_position()
            await websocket.send_text(f"{m_pos}")
            #if m_pose is not None:
            #    await websocket.send_text(f"Machine position: {m_pose}")
            #else:
            #    await websocket.send_text(f"Machine position: none")
    except Exception as e:
        print(e)
##ser.reset_input_buffer()


#cnc.home_machine()
#origin_px, top_right_pt, point_px = cnc.get_markers()
#if origin_px is not None:
    #px_per_mm = cnc.calc_px_per_mm(origin_px, top_right_pt, cnc.MARKER_SIZE_MM)
    #draw_x(120, 90, 5)
    #cnc.move_machine(point_px, origin_px, px_per_mm)
#else:
    #print("No markers found")

#input("  Press <Enter> to exit and disable grbl.")

# close serial
#cnc.s.close()

```
