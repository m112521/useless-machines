#include <AccelStepper.h>
#define limitX 9 //Limit pins: X->9 , Y->10 , Z->11

AccelStepper Xaxis(1, 2, 5); // pin 2 = step, pin 5 = direction // Y: step=3, dir=6; // Z: step=4 dir=7
AccelStepper Yaxis(1, 3, 6);

const byte enablePin = 8;
const int speed = -1000;

void setup()
{
  pinMode(enablePin, OUTPUT);
  pinMode(limitX, INPUT);

  digitalWrite(enablePin, LOW);

  Xaxis.setMaxSpeed(12800);
  Xaxis.setSpeed(speed); // 1000

  Yaxis.setMaxSpeed(12800);
  Yaxis.setSpeed(1000);

  Serial.begin(9600);
}

void loop()
{
  Xaxis.runSpeed();
  int endX = digitalRead(limitX);

  if (endX) {
    Xaxis.setSpeed(-speed);
  }

  // delay(2000);
  // Xaxis.stop();
  // Yaxis.runSpeed();
}