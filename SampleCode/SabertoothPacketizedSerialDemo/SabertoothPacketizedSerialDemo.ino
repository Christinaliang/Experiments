/* 
/ This is a simple Arduino program that demonstrates the
/ "Packetized Serial" method of using the Sabertooth Motor
/ Controller. 
/
/ SETUP: Be sure that the Sabertooth has DIPs 3,4,5,6 on (1,2 off).
/ Sabertooth should be connected on S1 to TX3 on an Arduino Mega 2560.
/ This allows it to read 9600-baud commands from the Arduino Mega.
/ Be careful to use TX3: TX1 should be reserved for Arduino-Computer
/ communications.
*/

// Variable to store how many milliseconds have passed.
int count = 0;

// We'll track which direction we're currently moving in this demo
// So we don't have to write more packets than we have to.
const unsigned int FORWARD_LABEL = 1;
const unsigned int BACKWARD_LABEL = 2;

int direction = BACKWARD_LABEL;
// Motor constants (used to communicate with the onboard computer).
const unsigned char FRONT_LEFT_DRIVE_MOTOR_ID = 0;
const unsigned char FRONT_RIGHT_DRIVE_MOTOR_ID = 1;
const unsigned char MIDDLE_LEFT_DRIVE_MOTOR_ID = 2;
const unsigned char MIDDLE_RIGHT_DRIVE_MOTOR_ID = 3;
const unsigned char REAR_LEFT_DRIVE_MOTOR_ID = 4;
const unsigned char REAR_RIGHT_DRIVE_MOTOR_ID = 5;

// Motor addressing (used to link the computer-constants to
// commands sent to the saberteeth).
const unsigned char FRONT_LEFT_DRIVE_MOTOR_ADDRESS = 128;
const unsigned char FRONT_RIGHT_DRIVE_MOTOR_ADDRESS = 128;
const unsigned char MIDDLE_LEFT_DRIVE_MOTOR_ADDRESS = 129;
const unsigned char MIDDLE_RIGHT_DRIVE_MOTOR_ADDRESS = 129;
const unsigned char REAR_LEFT_DRIVE_MOTOR_ADDRESS = 130;
const unsigned char REAR_RIGHT_DRIVE_MOTOR_ADDRESS = 130;

// Motor addressing offset: If a motor is connected to M1, 
// This will be 0. If the motor is connected to M2, this should
// be 4.
const unsigned char FRONT_LEFT_DRIVE_MOTOR_COMMAND = 0;
const unsigned char FRONT_RIGHT_DRIVE_MOTOR_COMMAND = 4;
const unsigned char MIDDLE_LEFT_DRIVE_MOTOR_COMMAND = 0;
const unsigned char MIDDLE_RIGHT_DRIVE_MOTOR_COMMAND = 4;
const unsigned char REAR_LEFT_DRIVE_MOTOR_COMMAND = 0;
const unsigned char REAR_RIGHT_DRIVE_MOTOR_COMMAND = 4;

// shorthand that will allow us to use the motor ID as an array index to access
// the relevant constants.
const unsigned char DRIVE_MOTOR_ADDRESS[6] = {
FRONT_LEFT_DRIVE_MOTOR_ADDRESS,
FRONT_RIGHT_DRIVE_MOTOR_ADDRESS,
MIDDLE_LEFT_DRIVE_MOTOR_ADDRESS,
MIDDLE_RIGHT_DRIVE_MOTOR_ADDRESS,
REAR_LEFT_DRIVE_MOTOR_ADDRESS,
REAR_RIGHT_DRIVE_MOTOR_ADDRESS};
const unsigned char DRIVE_MOTOR_COMMAND[6] = {
FRONT_LEFT_DRIVE_MOTOR_COMMAND,
FRONT_RIGHT_DRIVE_MOTOR_COMMAND,
MIDDLE_LEFT_DRIVE_MOTOR_COMMAND,
MIDDLE_RIGHT_DRIVE_MOTOR_COMMAND,
REAR_LEFT_DRIVE_MOTOR_COMMAND,
REAR_RIGHT_DRIVE_MOTOR_COMMAND};

void setup(){
  // Communicate with the computer
  Serial.begin(9600);
  // Communicate with the Sabertooth
  Serial3.begin(9600);
  count = 0;
}

// This program rotates a motor in alternating directions
// at ~90% power on a ~3 second cadence. 
void loop(){
  // Count how many milliseconds have passed
  count = count + 1;
  
  // First 3 seconds: Rotate one direction.
  // Second 3 seconds: Rotate the opposite direction.
  // After 6 seconds, repeat.
  if(count < 3000) {
    // If the last move was backwards, we need to change direction.
    if(BACKWARD_LABEL == direction){
      driveForwards(40,FRONT_LEFT_DRIVE_MOTOR_ID);
      driveForwards(40,MIDDLE_LEFT_DRIVE_MOTOR_ID);
      driveForwards(40,REAR_LEFT_DRIVE_MOTOR_ID);
      direction = FORWARD_LABEL;
    }
  } else if (count < 6000) {
    // If the last move was forwards, we need to change direction.
    if(FORWARD_LABEL == direction){
      driveBackwards(40,FRONT_LEFT_DRIVE_MOTOR_ID);
      driveBackwards(40,MIDDLE_LEFT_DRIVE_MOTOR_ID);
      driveBackwards(40,REAR_LEFT_DRIVE_MOTOR_ID);
      direction = BACKWARD_LABEL;
    }
  }
  else {
   count = 0; 
  }
  
  // Avoid overloading the motor controller.
  delayMicroseconds(1000);
  
}


// Function to drive forward. 
// Packet format: Address Byte, Command Byte, Value Byte, Checksum.
void driveForwards(unsigned char speed, char motor){
  unsigned char address = DRIVE_MOTOR_ADDRESS[motor];
  unsigned char command = DRIVE_MOTOR_COMMAND[motor];
  unsigned char checksum = (address + command + speed) & 0b01111111;
  Serial3.write(address);
  Serial3.write(command);
  Serial3.write(speed);
  Serial3.write(checksum);
}
void driveBackwards(char speed, char motor){
  unsigned char address = DRIVE_MOTOR_ADDRESS[motor];
  unsigned char command = DRIVE_MOTOR_COMMAND[motor] + 1;
  unsigned char checksum = (address + command + speed) & 0b01111111;
  Serial3.write(address);
  Serial3.write(command);
  Serial3.write(speed);
  Serial3.write(checksum);
}
  
  
