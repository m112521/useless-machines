G21 ; millimeters
G90 ; absolute coordinate
G17 ; XY plane
G94 ; units per minute feed rate mode
M3 S50; Turning on spindle


; Go to zero location
G0 X0 Y0

; Create rectangle
G1 X0 Y0 F1000
G1 Y10
G1 X10
G1 Y0
G1 X0

; Turning off spindle
M5
