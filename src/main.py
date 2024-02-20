import serial
import time
import json
from fastapi import FastAPI, Response, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import cv_grbl_aruco as cnc


origins = ["*"]
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

cnc.home_machine()
origin_px, top_right_pt, cameraMatrix, dist, origin_px_u = cnc.get_marker()
PX_PER_MM = cnc.calc_px_per_mm(origin_px, top_right_pt, cnc.MARKER_SIZE_MM)

m_pos = 0
p_point = "0.000,0.000,0.000"
points = []

cv_none = True

#@app.on_event('startup')
#def init_data():
#    pass

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global m_pos
    global cnc
    global p_point
    global origin_px
    global points
    global cv_none

    await websocket.accept()
    try:
        while True:
            point_gh = await websocket.receive_text()
            m_pos = cnc.get_machine_position()

            if cv_none:
                points = cnc.get_all_markers(origin_px, PX_PER_MM, cameraMatrix, dist, origin_px_u)
                cv_none = False

            await websocket.send_text(f"{m_pos}*{json.dumps(points)}")

            # Option 1: receive Point 3D from Ghrasshopper
            #print("Yo")
            if point_gh and p_point != point_gh:
                point3d = point_gh.split(",")
                print(float(point3d[0]), float(point3d[1]))
                p_point = point_gh
                cnc.move_machine_gh(float(point3d[0]), float(point3d[1]))


            # Option 2: CV markers or circles
            # get_markers() -> queue them all
            # move_machine to each

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