#include <Encoder.h>

Encoder e();
int previousPosition = 0;
void setup() {
  // put your setup code here, to run once:
  Encoder::setupEncoder();
  Serial.begin (9600);
  Serial.println("\n");
  Serial.println("Encoder demo is Ready.");
}

void loop() {
  // put your main code here, to run repeatedly:
    int val = Encoder::getPosition();
    int rot = Encoder::getRotationDirection();
    if(val != previousPosition)
    {
      Serial.print(val, DEC);
      Serial.print(rot == -1 ? "  clockwise" : "  counter-clockwise");
      Serial.print("\n");
      previousPosition = val;
    }
    delayMicroseconds(10000);
}
