/* 
/ This is a simple Arduino program that demonstrates the
/ "Simple Serial" method of using the Sabertooth Motor
/ Controller. 
/
/ SETUP: Be sure that the Sabertooth has DIPs 1,3,5,6 on (2,4 off).
/ Sabertooth should be connected on S1 to TX3 on an Arduino Mega 2560.
/ This allows it to read 9600-baud commands from the Arduino Mega.
/ Be careful to use TX3: TX1 should be reserved for Arduino-Computer
/ communications.
*/

// Variable to store how many milliseconds have passed.
int count = 0;

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
    Serial3.write(120);
  } else if (count < 6000) {
    Serial3.write(10);
  }
  else {
   count = 0; 
  }
  
  // Avoid overloading the motor controller.
  delayMicroseconds(1000);
  
}
  
