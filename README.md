# Useless Machines WP

> A useless machine is a device which has a function but no direct purpose (a guy from MIT)

Heavily inspired by Nadya Peek's Modular Machines and those guys from GitHub (I took the pulley and the rack from them)

TBD:
- [ ] wires enclosing
- [ ] insert m3 epoxy for table screwable
- [ ] Basement for the whole machine
- [ ] Calib Z via Camera
- [ ] PCBTraceGenerator.gh  -> G-code

- [ ] PCB ESP32 MotorShield milling test
- [ ] Gh non-planar milling (polystyrene) -> Gcode
- [ ] Gh Machine Generator with Young's modulus calculator
- [ ] Poopirka

- [ ] Wiring and test for H-bot (2xY)
- [ ] Printable KIT with brims + CV(arucoQR, bridge, RPiholder) + box(?)
- [ ] Knowledge graph: from abstraction to details


- [x] Gh collision simulation
- [x] RPi Pyserial to GRBL  
- [x] Modular linear axes (MLA)
- [x] MLA XY+ assembly
- [x] TCP to point2D using OpenCV
- [x] Gh SyncSim WS

- [x] fix tool holder
- [x] Add endstop hole
- [x] Make axis supports fastanable to axis and to the floor
- [x] Yong's modulus for 12, 18 plywood


Functionality check:
- [ ] CV weaving 
- [ ] Web/PDF WP
- [ ] Dremel Z -> PCBTraceGenerator.gh
- [ ] p5.js lib -> draw and gcode stream
https://docs.google.com/document/d/1zGq897flr5F2EenAS7bOPgM9schD1iEFRFdtpmhVqJQ/edit

![Simulation](imgs/gh-sim.gif)

CNC Shield/GRBL config:

1. CNC Shield Jumpers
2. GRBL spindle speed


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

-------------------------------------

Instructions:


Carrige 1:

https://github.com/m112521/useless-machines/assets/85460283/1d898f0c-5cae-43d9-b15b-1ca97f9952e6

Carrige 2:

https://github.com/m112521/useless-machines/assets/85460283/568b16e4-cb6c-4cd2-8910-7a5e2f30e3df


Carrige 3:

https://github.com/m112521/useless-machines/assets/85460283/dc9f5c50-31b6-4a93-bcf2-43fd21f10367


Carrige 4:

https://github.com/m112521/useless-machines/assets/85460283/1df0a3c2-96c0-4288-9bb8-245eb9bfb2f2


Rail: 

https://github.com/m112521/useless-machines/assets/85460283/70a19164-39d7-4d2d-80c0-af41929da47c


Axis X-1:

https://github.com/m112521/useless-machines/assets/85460283/7156194f-57ff-49da-a9d0-40450719a380


Axis X-2:

https://github.com/m112521/useless-machines/assets/85460283/d27853ad-4865-437f-8faa-c0686a177267



Axis X-endstop:

https://github.com/m112521/useless-machines/assets/85460283/16b9a3ca-a30e-440b-8486-f2dd495ec5e4


Axis XV-support:

https://github.com/m112521/useless-machines/assets/85460283/c26f3623-e518-4918-be77-d1f35b5745ff


Wheel-X:

https://github.com/m112521/useless-machines/assets/85460283/9568cd56-e5c2-4810-b618-4dbb1be0e70f


Carrige VY-holderVX

https://github.com/m112521/useless-machines/assets/85460283/4576e473-dfea-46f0-a778-e4fb95ce2ffa


Assembly VY-VX:

https://github.com/m112521/useless-machines/assets/85460283/b02ba156-daf3-4695-9696-71cce22d752f


Assembly-VX-FOR-HY:

https://github.com/m112521/useless-machines/assets/85460283/e208e78f-c716-4a84-b4d4-77ff1d42ef49


Assembly-VXHY:

https://github.com/m112521/useless-machines/assets/85460283/3cd34c90-32d5-4921-98f5-b61b05a48a90


