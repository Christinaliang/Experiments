/*
 * Author: Alex Schendel
 * 29 March 2018
 * Arduino sketch to control servo motor.
 * Use digital input?
 */

#include <Servo.h>//include the servo header file to allow the use of servos

Servo servo;//create a servo object
int servoPin=9;
int pos = 0;//integer to store position in degrees(for loop iterator) 
int scanDelay = 15;//May need to increase delay for scanning...

void setup() {
  Serial.begin(9600);//start the serial on the 9600 band
  servo.attach(servoPin);//attach servo to pin 9
}

void loop() {
  // put your main code here, to run repeatedly:
  
}
