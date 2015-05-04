/* PowerScrewDriver

Authors: Derek Schumacher, Fatima Dominguez, Jaimiey Sears

Reads in a degree value from serial and translates it to
a number of steps that will translate the linear power
screws the desired percentage

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

int DIRECTION_PIN = 8;
int PULSE_PIN = 9;
int ENABLE = 10;

//31914 steps translates to roughly (under) 100% top to bottom
int FULL_STEPS = 31914;
int stepCount = 0;
int desiredPercent = 0;
//double onePercent = 1 / FULL_STEPS;
int desiredStep = 0;
int DELAY = 10;

//variable which disables all motor movement when set to TRUE.
boolean e_stop = false;

void setup() {

  pinMode(DIRECTION_PIN, OUTPUT);
  pinMode(PULSE_PIN, OUTPUT);
  pinMode(ENABLE, OUTPUT);
  //  digitalWrite(ENABLE, HIGH); //the motor should not make loud screeching
  Serial.begin(9600);
  Serial.println("Enter Linear distance as a percentage:");
}//setup

void loop() {

  if (Serial.available())
  {
    desiredPercent = Serial.parseInt();

    if (abs(desiredPercent) > 100) {
      Serial.println("that value is outside of the operable range");
    }
    else {
      desiredStep = int(desiredPercent / 100.0 * FULL_STEPS);
      Serial.print("Distance to move: ");
      Serial.print(desiredPercent);
      Serial.print(" % \t");
      Serial.print("Number of Steps: ");
      Serial.println(desiredStep);
      stepCount = 0;
      rotate();
    }
  }
  e_stop = false;
}//loop

void rotate() {
  //enable the controller
  digitalWrite(ENABLE, LOW);
  //  delayMicroseconds(1000000);
  if (desiredStep > 0) digitalWrite(DIRECTION_PIN, LOW);
  else digitalWrite(DIRECTION_PIN, HIGH);
  //    delayMicroseconds(DELAY);
  //    digitalWrite(DIRECTION_PIN,HIGH);

  delayMicroseconds(DELAY);

  while (stepCount < abs(desiredStep)) {
    delayMicroseconds(DELAY);
    digitalWrite(PULSE_PIN, HIGH);
    delayMicroseconds(DELAY);
    digitalWrite(PULSE_PIN, LOW);

    //leave if we say so
    interrupt();
    if (e_stop) break;

    //wait for 100 ms
    delayMicroseconds(1000000);
    stepCount++;
  }

  digitalWrite(ENABLE, HIGH);

}

//used to read any commands that have been recieved
void interrupt() {
  if (Serial.available()) {
    char command = Serial.read();
    switch (command) {
      case 's':
        e_stop = true;
        break;
      case 'S':
        e_stop = true;
        break;
    }
  }
}
