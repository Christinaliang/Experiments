//Just a test. Slowly moves from START_POS to END_POS, then goes max speed back to START_POS

#include <Servo.h>//include the servo header file to allow the use of servos

Servo servo;//create a servo object
int servoPin=9;
const int MID = 90;
const int START_POS = MID+30;
const int END_POS = MID-40;
int pos = START_POS;//integer to store position in degrees(for loop iterator)
int scanDelay = 30;//May need to increase delay for scanning...

void setup() {
  servo.attach(servoPin);//attach servo to pin 9
  servo.write(pos);
  delay(scanDelay);
}

void loop() {
  if(pos>END_POS){
    pos--;
    servo.write(pos);
    delay(scanDelay);
  }
  else if(pos<=END_POS){
    pos=START_POS;
    servo.write(pos);
    delay(1000);
  }
}
