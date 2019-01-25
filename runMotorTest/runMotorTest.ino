unsigned char wheelID[15] =  {133, 132, 131, 130, 129, 128,         //Drive motors
                              133, 132, 131, 130, 129, 128,         //articulation motors
                              134,   0, 134};                       //Misc motors

const int FORWARD_DRIVE = 0;   //Command sent for Clockwise rotation for drive wheels (Motor 1)
const int BACKWARD_DRIVE =1;   //Command sent for Counter-Clockwise rotation for drive wheels (Motor 1)
const int FORWARD_ART = 4;     //Command sent for Clockwise rotation for articulation wheels (Motor 2)
const int BACKWARD_ART =5;     //Command sent Counter-Clockwise rotation for articulation wheels (Motor 2)

void setup() {
  Serial.begin(9600);//CHECK BAUD RATE
}

void loop(){
  runMotor();
}

void runMotor(){
  unsigned char address = 128;//motor controller address (between 128 and 135)
  unsigned char command = FORWARD_ART;//command: 0 Motor 1 forward, 1 Motor 1 backward, 4 Motor 2 forward, 5 Motor 2 backward. (Motor 1 is drive motor, Motor 2 is articulation motor)
  unsigned char data = 100;//speed from 0-127
  unsigned char checksum = (address + command + data) & 127;//error check. Sum address, command, and speed. Then, apply the bitwise AND operator on that and 127.
  Serial.write(address);//send all the values over the first Serial port. BYTE is used to make it send in binary representation.
  Serial.write(command);
  Serial.write(data);
  Serial.write(checksum);
  
}
