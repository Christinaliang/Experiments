/*
 * Author: Alex Schendel, Alex Reinemann
 * 29 March 2018
 * Arduino sketch to control servo motor.
 * Use ROS publisher/subscriber
 */

#include <Servo.h>//include the servo header file to allow the use of servos
#include <ros.h>//includes ROS header to allow use of publisher/subscriber
//include the pub/sub message format
#include <command2ros/ScanCommand.h>

Servo rohServo, raiseServo, thetaServo;//create a servo objects (roh is the scanning, theta is forwards or backwards, and raise is raising or lowering the mount.
int rohPin=9, thetaPin=10, raisePin=11;
int pos = 0;//integer to store position in degrees(for loop iterator) 
const int MID = 90;
const int START_POS = MID;
const int END_POS = MID-40;
int scanDelay = 1000;//May need to increase delay for scanning...
const int FRONT = 0;//for rotating LIDAR, can do front scan or back scan
const int BACK = 180;
const int DOWN = 0;//for the raising and lowering of the LIDAR mount.
const int UP = 90;
int id=0;
bool isComplete = false;//if scan is complete, go back to initial state
ros::NodeHandle nh;

void messageCb(const command2ros::ScanCommand& scan_msg){
  if(id != scan_msg.serialID){//if we get a new message
    id = scan_msg.serialID;
    isComplete = false;//reset everything to initial state
    //scan();
    pos=START_POS;
    rohServo.write(pos);
    if(scan_msg.scan){//and rotate to the correct direction to scan front or back
      thetaServo.write(FRONT);//rotate to front
    }
    else{
      thetaServo.write(BACK);//rotate to back
    }
  }
}

ros::Subscriber<command2ros::ScanCommand> sub("Scan", &messageCb);

void setup() {
  rohServo.attach(rohPin);//attach servo to pin 9
  thetaServo.attach(thetaPin);//attach servo to pin 10
  raiseServo.attach(raisePin);//attach servo to pin 11
  raiseServo.write(UP);
  Serial.begin(57600);
  nh.initNode();
  nh.subscribe(sub);
}

/*void scan() {
  if(pos <= END_POS){
    pos = START_POS;
    servo.write(pos);
  }
  else{
    pos=pos+1;
    servo.write(pos);
  }
}*/

void scan() {
  if(pos <= END_POS){
    isComplete = true;
  }
  if(!isComplete){
    pos -= 1;
    rohServo.write(pos);
    delay(scanDelay);
  }
  else if(isComplete){
    pos = START_POS;
    rohServo.write(pos);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  scan();
}
