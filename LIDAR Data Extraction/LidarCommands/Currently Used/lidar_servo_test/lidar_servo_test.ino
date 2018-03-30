/*
 * Author: Alex Schendel
 * 28 March 2018
 * Sweeps a servo motor on pin 9
 */

#include <Servo.h>//include the servo header file to allow the use of servos

Servo servo;//create a servo object
int pos = 0;//integer to store position in degrees(for loop iterator)
int delayms=700;//delay time in ms

void setup() {
  Serial.begin(9600);//start the serial on the 9600 band
  servo.attach(9);//attach servo to pin 9
}

void loop() {
  Serial.println("Start 0 to 180");//print over the serial (appears in the serial monitor
  /*for(pos=0; pos<=180; pos+=1){//0 to 180 degrees
    servo.write(pos);//tell servo to goto pos
    delay(delayms);//wait specified ms
  }*/
  servo.write(180);
  delay(delayms);
  Serial.println("Start 180 to 0");
  /*for(pos=180; pos>=0; pos-=1){//180 to 0 degrees
    servo.write(pos);//tell servo to goto pos
    delay(delayms);//wait specified ms
  }*/
  servo.write(0);
  delay(delayms);
}
