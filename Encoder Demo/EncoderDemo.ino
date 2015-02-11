/* Read Encoder data
* Connect an Encoder and spits out what it is reading in degrees. 
*
* NOTES: 
*   reminder to connect +5V and ground to the arduino.
*   CW Rotation if A leads B, CCW Rotation if B leads A
*   can timing considerations cause bugs?
*/

const int encoderPinA = 3;
const int encoderPinB = 4;
const int encoderPinIndex = 7;
const int encoderPinLED = 5;

int previousAValue = LOW;
int previousBValue = LOW;
int encoderPos =  0;

void setup() {
  pinMode (encoderPinA, INPUT);
  pinMode (encoderPinB, INPUT);
  pinMode (encoderPinIndex, INPUT);
  pinMode (encoderPinLED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int currentAValue = digitalRead(encoderPinA);
  
   
    //See if we have a rising edge for A. If we do, and 
    //B is low, it means A is leading B, else B is leading A:
  if (previousAValue == LOW && currentAValue == HIGH) {
    if (digitalRead(encoderPinB) == LOW) {
        encoderPos--;
        Serial.println("CCW");
        //TODO turn on LED for counter-clockwise
        
    } else {
      encoderPos++;
      //TODO turn on LED for clockwise
      Serial.println("CW");
    }
    Serial.print("Encoder position: ");
    Serial.println(encoderPos);
  }
  
   //See if the index has gone off. Turn on LED if it has and reset pos
   if(digitalRead(encoderPinIndex) == HIGH) {
    //TODO turn on LED for index
    encoderPos = 0;
    Serial.println("Index changed. Full rotation achieved.");
  }
  
  //Store the current A value
  previousAValue = currentAValue;
  
 
}
