/****************************************************************************************

Author:    Brenda A Bell
Modified by Derek Schumacher on March 24, 2015

****************************************************************************************/

#define ENCODER0PINA         3      // this pin needs to support interrupts
#define ENCODER0PINB         4     // no interrupt required
#define ENCODER0INDEX        2      //interrupt required
#define CPR                  400    // encoder cycles per revolution
#define CLOCKWISE            2       // direction constant
#define COUNTER_CLOCKWISE    1       // direction constant

// variables modified by interrupt handler must be declared as volatile
volatile long encoder0Position = 0;
volatile long interruptsReceived = 0;
volatile long numRotations = 0;

// track direction: 0 = counter-clockwise; 1 = clockwise
short currentDirection = CLOCKWISE;

// track last position so we know whether it's worth printing new output
long previousPosition = 0;

void setup()
{

  // inputs
  pinMode(ENCODER0PINA, INPUT);
  pinMode(ENCODER0PINB, INPUT);
  pinMode(ENCODER0INDEX, INPUT);
  
  // interrupts
  attachInterrupt(1, onInterrupt, RISING);
  attachInterrupt(0, onIndexChanged, RISING);

  // enable diagnostic output
  Serial.begin (9600);
  Serial.println("\n\n\n");
  Serial.println("Ready.");
}

void loop()
{
  // only display position info if has changed
  if (encoder0Position != previousPosition )
  {
    Serial.print(encoder0Position, DEC);
    Serial.print("\t");
    Serial.print(currentDirection == CLOCKWISE ? "clockwise" : "counter-clockwise");
    Serial.print("\t");
    Serial.println(interruptsReceived, DEC);
    previousPosition = encoder0Position;
  }
}

// interrupt function needs to do as little as possible
void onInterrupt()
{
  // read both inputs
  int a = digitalRead(ENCODER0PINA);
  int b = digitalRead(ENCODER0PINB);
    
  if (a == b )
  {
    // b is leading a (counter-clockwise)
    encoder0Position--;
    currentDirection = COUNTER_CLOCKWISE;
  }
  else
  {
    // a is leading b (clockwise)
    encoder0Position++;
    currentDirection = CLOCKWISE;
  }

  // track 0 to 400
  encoder0Position = encoder0Position % CPR;

  // track the number of interrupts
  interruptsReceived++;
}

void onIndexChanged()
{
    //If we hit the index, display that information.
  Serial.print("Hit Index. Num revolutions: ");
  Serial.println(numRotations);
  numRotations++;
}
