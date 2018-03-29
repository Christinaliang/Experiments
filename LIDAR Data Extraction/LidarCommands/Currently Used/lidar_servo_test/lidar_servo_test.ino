#include <Servo.h>

Servo servo;
int pos = 0;

void setup() {
  servo.attach(9);
}

void loop() {
  for(pos=0; pos<=180; pos+=1){//0 to 180 degrees
    servo.write(pos);//tell servo to goto pos
    delay(15);//wait 15 ms
  }
  for(pos=180; pos>=0; pos-=1){//180 to 0 degrees
    servo.write(pos);//tell servo to goto pos
    delay(15);//wait 15 ms
  }
}
