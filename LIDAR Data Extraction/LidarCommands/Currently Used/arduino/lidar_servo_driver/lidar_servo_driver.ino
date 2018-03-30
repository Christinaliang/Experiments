/*
 * Author: Alex Schendel
 * 29 March 2018
 * Arduino sketch to control servo motor.
 * Use ROS publisher/subscriber
 */

#include <Servo.h>//include the servo header file to allow the use of servos
#include <ros.h>//includes ROS header to allow use of publisher/subscriber
//include the pub/sub message format
#include <command2ros/ScanCommand.h>

Servo servo;//create a servo object
int servoPin=9;
int pos = 0;//integer to store position in degrees(for loop iterator) 
const int MID = 90;
const int START_POS = MID+30;
const int END_POS = MID-40;
int scanDelay = 15;//May need to increase delay for scanning...
const int FRONT = 0;//for rotating LIDAR, can do front scan or back scan
const int BACK = 180;
int id=0;
bool isComplete = false;//if scan is complete, go back to initial state

ros::NodeHandle nh;

void messageCb(const command2ros::ScanCommand& scan_msg){
  if(id != scan_msg.serialID){//if we get a new message
    id = scan_msg.serialID;
    isComplete = false;//reset everything to initial state
    pos=START_POS;
    servo.write(pos);
    if(scan_msg.scan){//and rotate to the correct direction to scan front or back
      //rotate to front
    }
    else{
      //rotate to back
    }
  }
}

ros::Subscriber<command2ros::ScanCommand> sub("scan_msg", &messageCb);

void setup() {
  servo.attach(servoPin);//attach servo to pin 9
  nh.initNode();
  nh.subscribe(sub);
}

void scan() {
  if(pos <= END_POS){
    isComplete = true;
  }
  if(!isComplete){
    pos -= 1;
    servo.write(pos);
    delay(scanDelay);
  }
  else if(isComplete){
    pos = START_POS;
    servo.write(pos);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  scan();
}
