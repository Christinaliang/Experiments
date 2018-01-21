/* BucketWheelActuationDriver

Authors: Derek Schumacher, Fatima Dominguez, Jaimiey Sears

Begins by assuming the bucket wheel is at its lowest point (100%)
The user can specify a percentage to actuate to (0-100%)

The circuit uses HSI power screws and Microstep Driver- M6128 :
DIP Switch: [111001] (1 = down, 0 = up)
[current: 1.25; Microstep = 1 (Full-step)]

Send an 's' or 'S' to e-stop screw movement

The wiring scheme for the HSI power screws:
Red (A+)
Red/White (A-)
Green (B+)
Green/white (B-)

PUL+ (pin 9)
DIR+ (pin 8)
PUL- and DIR- grounded

ENA+ connected to ground
ENA- connected to pin 10 (+5V when turning, otherwise 0V)

*/
#define ERROR_OUT_OF_RANGE -1

const int BUCKET_SABERTOOTH_ADDRESS = 1;


int DIRECTION_PIN = 8;
int PULSE_PIN = 9;
int ENABLE = 10;

//31914 steps translates to roughly (under) 100% top to bottom
#define FULL_STEPS 31914
//int stepCount = 0;
int desiredPercent = 0;

//double onePercent = FULL_STEPS/100.0;
//int desiredStep = 0;
int DELAY = 10;

//double currentPercent = 100;
int currentSteps = FULL_STEPS;

//variable which disables all motor movement when set to TRUE.
boolean e_stop = false;

void setup() {

  pinMode(DIRECTION_PIN, OUTPUT);
  pinMode(PULSE_PIN, OUTPUT);
  pinMode(ENABLE, OUTPUT);
  //  digitalWrite(ENABLE, HIGH); //the motor should not make loud screeching
  Serial3.begin(9600);
  
  Serial.begin(9600);
  Serial.println("Send position to go to (percent):");
  printPosition();
}//setup

void loop() {

  if (Serial.available())
  {
    char cmd = Serial.read();
    if (cmd == 'r' || cmd == 'R') {
      Serial.println("Enter a height for bucket wheel:");
      while (!Serial.available());
      int readValue = Serial.parseInt();
      moveToPercent(readValue);
    }
    
    if (cmd == 's' || cmd == 'S') {
      Serial.println("Enter a speed for bucket wheel:");
      while (!Serial.available());
      int readValue = Serial.parseInt();
      if (readValue >= 0) {
//        128
//        130
//        131
        //driveClockwise(int motorID, int speed, unsigned char command)
        driveClockwise(128, readValue, 1);
        driveClockwise(130, readValue, 1);
        driveClockwise(131, readValue, 1);
        Serial.println("Spinning bucketwheel clockwise");
      } else {
        driveCounterclockwise(128, -1*readValue, 0);
        driveCounterclockwise(130, -1*readValue, 0);
        driveCounterclockwise(131, -1*readValue, 0);
        Serial.println("Spinning bucketwheel counter-clockwise");
      }
    }

  }
  e_stop = false;
}//loop

//moves the wheel the down the number of steps specified
//negative steps will be interpred as moving the wheel up. 
void actuate(int steps) {
  //enable the controller
  digitalWrite(ENABLE, LOW);
  
  int dir = 0;
  //select which direction to go
  if (steps > 0) {
    digitalWrite(DIRECTION_PIN, LOW);
    dir = 1;
  }
  else {
    digitalWrite(DIRECTION_PIN, HIGH);
    dir = -1;
  }
  
  for(int i = 0; i < abs(steps); i++) {
    //leave if we say so
    interrupt();
    if (e_stop) break;
    
    //send pulse to controller
    delayMicroseconds(DELAY);
    digitalWrite(PULSE_PIN, HIGH);
    delayMicroseconds(DELAY);
    digitalWrite(PULSE_PIN, LOW);

    //update and print position as we move
    currentSteps += dir;
    //every 50,000 ms print new position
    if (i%500 == 0) printPosition();
    
    //wait for 100 ms
    delayMicroseconds(1000000);
  }
  //report final position
  printPosition();

  digitalWrite(ENABLE, HIGH);
}

//used to read any commands that have been recieved
void interrupt() {
  if (Serial.available()) {
    char command = Serial.read();
    switch (command) {
      //emergency stom if command == 's' or 'S'
      case 's':
        e_stop = true;
        break;
      case 'S':
        e_stop = true;
        break;
    }
  }
}

//short subroutine to print the current actuation position of the bucketwheel
void printPosition() {
  Serial.print("Current Position:\t");
  Serial.print(toPercent(currentSteps), DEC);
  Serial.println("%");
}


//moves to the given percent from the current position
int moveToPercent(int percent){
  //error check
  if (percent > 100 || percent < 0) return ERROR_OUT_OF_RANGE;
  
  //calculate number of steps and move.
  int stepsToMove = int(-(toPercent(currentSteps) - percent)/100.0 * FULL_STEPS);
  Serial.print("Moving to ");
  Serial.print(percent, DEC);
  Serial.print("% from ");
  Serial.print(toPercent(currentSteps), DEC);
  Serial.println("%");
  actuate(stepsToMove);
}

//takes a position in steps and converts it to a percentage
double toPercent(int steps) {
  return steps*100.0/FULL_STEPS;
}

/**
 * Drives a given motor at a given speed in a clockwise direction
 *
 * Paramteters:
 *  motorID - the id of the motor to spin (0-11)
 *  speed - the speed at which to spin the motor.
 */
void driveClockwise(int motorID, int speed, unsigned char command){

  
  // Packet format: Address Byte, Command Byte, Value Byte, Checksum.
  // Build the data packet:
  // Get the address and motor command ID from a predefined array.
  unsigned char address = motorID;
  // If the motor is connected backwards, we need to flip the command from 0/4 to 1/5:

  unsigned char checksum = (address + command + ((char)speed)) & 0b01111111;

  // Write the packet.
  Serial3.write(address);
  Serial3.write(command);
  Serial3.write(((char)speed));
  Serial3.write(checksum);
  //TODO: Move the delay time to a constant
  delayMicroseconds(1000); 
}

/**
 * Drives a given motor at a given speed in a counterclockwise direction
 *
 * Paramteters:
 *  motorID - the id of the motor to spin (0-11)
 *  speed - the speed at which to spin the motor.
 */
void driveCounterclockwise(char motorID, char speed, unsigned char command){ 

  // Packet format: Address Byte, Command Byte, Value Byte, Checksum.
  unsigned char address = motorID;
  // If the motor is connected backwards, we need to flip the command from 1/5 to 0/4:

  unsigned char checksum = (address + command + speed) & 0b01111111;
  Serial3.write(address);
  Serial3.write(command);
  Serial3.write(speed);
  Serial3.write(checksum);
  //TODO: Move the delay time to a constant
  delayMicroseconds(1000);
}


