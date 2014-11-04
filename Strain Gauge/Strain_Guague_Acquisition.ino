//Code for strain guague data acquisition...
#define GAUGUE_1 A0
#define GAUGUE_2 A1
#define GAUGUE_3 A2
#define GAUGUE_4 A3

#define NUM_SAMPLES 100
#define SAMPLING_RATE 100

  
void setup() {
 Serial.begin(9600);
}

int voltage1 = 0;
  int voltage2 = 0;
  int voltage3 = 0;
  int voltage4 = 0;

void loop() {
  pollGauges();
  Serial.write(voltage1);
  Serial.write(voltage2);
  Serial.write(voltage3);
  Serial.write(voltage4);
}

void pollGauges()
{
  static int V0 = 0;
  static int V1 = 0;
  static int V2 = 0;
  static int V3 = 0;
 
  
  for (int i = 0; i < NUM_SAMPLES; ++i)
  {
    V0 += analogRead(GAUGUE_1) / i;
    V1 += analogRead(GAUGUE_2) / i;
    V2 += analogRead(GAUGUE_3) / i;
    V3 += analogRead(GAUGUE_4) / i; 
    delay(SAMPLING_RATE); 
  }
  
  voltage1 = V0;
  voltage2 = V1;
  voltage3 = V2;
  voltage4 = V3;
}

void pollGauges_withStatisticalNoiseReduction()
{
  //"instantaneously" average from each voltage source. We'll need four arrays:
  static int V0 = 0;
  static int V1 = 0;
  static int V2 = 0;
  static int V3 = 0;
 
  static int voltage1[100];
  static int voltage2[100];
  static int voltage3[100];
  static int voltage4[100];
 
  
  for (int i = 0; i < NUM_SAMPLES; ++i)
  {
    voltage1[i] += analogRead(GAUGUE_1) / i;
    voltage2[i] += analogRead(GAUGUE_2) / i;
    voltage3[i] += analogRead(GAUGUE_3) / i;
    voltage4[i] += analogRead(GAUGUE_4) / i; 
    delay(SAMPLING_RATE); 
  }
  
  //We're going to do some questionable statistics to remove noise....
  //Hang on!
  
  /*
  static int cdf[100];
  
  //First, generate a CDF for each guage (while inverting it of course!):
  for (int i = 0; i < NUM_SAMPLES; ++i)
  {
    cdf[i] = 1/computeCDF(i);
  }
  
  //Now use our CDF to check and thrown away outliers...if things don't sit
  //in the middle band of the CDF, toss them:
  for (int i = 0; i < NUM_SAMPLES; ++i)
  {
    
  }
  
  */
}
/*
int computeCDF(int index)
{
  int sum = 0;
    
  if (index == 0)
  {
    sum = voltage[index];
    return sum;
  }  
    
  for (int i = 0; i < index; ++i)
  {
    sum += voltage1[i];
  }
  
  return sum;
}

//Computes the probability of finding that voltage:
int computePDF(int value)
{
  //Base case: we have found the upper bound.
  //if upper bound, stop. if upper bound > threshold or if lower
  //bound is less than lower threshold, throw it away!
  
 }
 */
