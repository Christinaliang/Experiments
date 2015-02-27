/* StepperMotorDrive

Authors: Derek Schumacher and Fatima Dominguez

Reads in a degree value from serial and translates it to 
a number of steps that will rotate the motor to the desired 
degree.

The circuit using a NEMA 14 and Microstep Driver- M6128 :
[current: 1.25; Microstep = 1 (Full-step)]

Red (A+)
Green (A-)
Yellow (B+)
Blue (B-)

PUL+ (pin 8)
DIR+ (pin 9)

ENA+ connected to ground
ENA- connected to pin 10 (+5V when turning, otherwise 0V)

*/


int DIRECTION_PIN = 8;
int PULSE_PIN = 9;
int ENABLE = 10;
int stepCount = 0;
int desiredDegrees = 0;
double stepDegree = 0.094;
int desiredStep = 0;
int DELAY = 100;

void setup(){

  pinMode(DIRECTION_PIN, OUTPUT);
  pinMode(PULSE_PIN, OUTPUT);
  pinMode(ENABLE, OUTPUT);
  digitalWrite(ENABLE, HIGH); //the motor should not make loud screeching
  Serial.begin(9600);
}

void loop() {

  if(Serial.available())
  {
    desiredDegrees = Serial.parseInt();
    desiredStep = int(desiredDegrees/stepDegree);
    Serial.print("Number of Steps: ");
    Serial.println(desiredStep); 
    stepCount = 0;
    digitalWrite(ENABLE,LOW);
  }
  
  if(stepCount < desiredStep){
    digitalWrite(DIRECTION_PIN, HIGH);
    delayMicroseconds(DELAY);
    digitalWrite(DIRECTION_PIN,LOW);

    delayMicroseconds(DELAY);

    digitalWrite(PULSE_PIN, HIGH);
    delayMicroseconds(DELAY);
    digitalWrite(PULSE_PIN, LOW);

    delayMicroseconds(1000000);
    stepCount++;
  }

}
