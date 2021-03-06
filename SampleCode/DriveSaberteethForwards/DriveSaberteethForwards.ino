/* 
 / This is a simple Arduino program that drives all the 
 / drive motors on the transporter forwards at the specified
 / power value.
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
const unsigned char FRONT_LEFT_DRIVE_MOTOR_ADDRESS = 129;
const unsigned char FRONT_RIGHT_DRIVE_MOTOR_ADDRESS = 130;
const unsigned char MIDDLE_LEFT_DRIVE_MOTOR_ADDRESS = 130;
const unsigned char MIDDLE_RIGHT_DRIVE_MOTOR_ADDRESS = 129;
const unsigned char REAR_LEFT_DRIVE_MOTOR_ADDRESS = 128;
const unsigned char REAR_RIGHT_DRIVE_MOTOR_ADDRESS = 128;

// Motor addressing offset: If a motor is connected to M1, 
// This will be 0. If the motor is connected to M2, this should
// be 4.
const unsigned char FRONT_LEFT_DRIVE_MOTOR_COMMAND = 4;
const unsigned char FRONT_RIGHT_DRIVE_MOTOR_COMMAND = 0;
const unsigned char MIDDLE_LEFT_DRIVE_MOTOR_COMMAND = 4;
const unsigned char MIDDLE_RIGHT_DRIVE_MOTOR_COMMAND = 0;
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

// This program drives forward.
void loop(){
    // If the last move was backwards, we need to change direction.
    if(BACKWARD_LABEL == direction){
      unsigned char speed = 120;
      driveForwards(speed, FRONT_LEFT_DRIVE_MOTOR_ID);
      driveForwards(speed, FRONT_RIGHT_DRIVE_MOTOR_ID);
      driveForwards(speed, MIDDLE_LEFT_DRIVE_MOTOR_ID);
      driveForwards(speed, MIDDLE_RIGHT_DRIVE_MOTOR_ID);
      driveForwards(speed, REAR_LEFT_DRIVE_MOTOR_ID);
      driveForwards(speed, REAR_RIGHT_DRIVE_MOTOR_ID);
      direction = FORWARD_LABEL;
    }
  // Avoid overloading the motor controller.
  delayMicroseconds(1000);

}

// Function to drive forward. 
// Packet format: Address Byte, Command Byte, Value Byte, Checksum.
void driveForwards(unsigned char speed, char motor){
  // Build the data packet:
  // Get the address and motor command ID from a predefined array.
  unsigned char address = DRIVE_MOTOR_ADDRESS[motor];
  unsigned char command = DRIVE_MOTOR_COMMAND[motor];
  unsigned char checksum = (address + command + speed) & 0b01111111;
  // Write the packet.
  Serial3.write(address);
  Serial3.write(command);
  Serial3.write(speed);
  Serial3.write(checksum);
}
