/* Demo code to read data from current sensor.
Autor: Derek Schumacher 03.05.2015

NOTE: ACS714LLCTR-20A-T +- 20 A range, 100 mV/A
      ACS714LLCTR-30A-T +-30 A range, 66 mV/A
      MEASURED EQUATION: 11.525 * VOLTAGE - 29.4
*/

static int voltsPerAmp = 87; //mV/A

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
}

void loop() {
  
  double voltage = 0;
  double current = 0;
  bool reading = true;
  
    voltage = (analogRead(A0)* (5.0/1023.0));
    if(voltage > 2.56) {
      current = currentValue(voltage);
    }else {
     current = 0; 
    }
   
   Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.print(" Current: ");
  Serial.println(current);
  
  
  //Serial.print("Voltage: ");
  //Serial.print(voltage);
  //Serial.print(" Current: ");
  //Serial.println(current);
}

double currentValue(double voltage) {
   return 11.525*voltage - 29.4; 
}
