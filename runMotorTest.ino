unsigned char wheelID[15] =  {133, 132, 131, 130, 129, 128,         //Drive motors
                              133, 132, 131, 130, 129, 128,         //articulation motors
                              134,   0, 134};                       //Misc motors
const int wheelPinType[15] = {1, 1, 1, 1, 1, 1,
                              2, 2, 2, 2, 2, 2,
                              2, 1, 1};

boolean wheelDirection[15] = {false, true, false, true, false, false,   //Drive motors
                              false, true, false, true, true,  false, //articulation motors
                              true,  true, false};                    //Misc motors

double wheelCorectFactor[15] =  {1.11, 1.20, 1.12, 1.07, 1.05, 1.07, //Drive motors
                                 2.00, 1.15, 1.30, 1.15, 1.10, 1.20,  //articulation motors
                                 1.0, 1.0, 1.0};                      //Misc motors

boolean FORWARD = true;   //Clockwise rotation
boolean BACKWARD = false; //Counter-Clockwise rotation
//These need special ints to control moter rotations
const int FORWARD_DRIVE = 1;   //Clockwise rotation for drive wheels
const int BACKWARD_DRIVE =0;   //Counter-Clockwise rotation for drive wheels
const int FORWARD_ART = 4;     //Clockwise rotation for articulation wheels
const int BACKWARD_ART =5;     //Counter-Clockwise rotation for articulation wheels
boolean ardCancel = false;

void setup() {
  Serial.begin(38400);
  
}

void loop(){
  runMotor(128, true, 30); 
}

void runMotor(int ID, int commandInt, int tempSpeed){ //=====================================================================================================
  //If we are Paused or canceled, do not allow any Motor to run, only stop motor
  if(ardCancel == true && tempSpeed != 0){return;}
  //if(ardPause && tempSpeed != 0){return;}

  //int speed = tempSpeed;
//  if(wheelPinType[ID] == 2){
//    speed = 255 - tempSpeed;
//  }
  
  unsigned char address = wheelID[ID];
  unsigned char command;
  //reverse the wheels direction if need be
  if(wheelPinType[ID] == 1){
    //Move Drive Motor
    if((wheelDirection[ID] == true && commandInt == FORWARD) || 
       (wheelDirection[ID] == false && commandInt == BACKWARD)){
      //Drive FORWARD (Clockwise)
      command = (char)FORWARD_DRIVE;
    }
    else if ((wheelDirection[ID] == true && commandInt == BACKWARD) ||
             (wheelDirection[ID] == false && commandInt == FORWARD)){
      //Drive Backward (Counter-Clockwise)
      command = (char)BACKWARD_DRIVE;
    }
    
  }
  else if(wheelPinType[ID] == 2){
    //Move Articulation Motor
    if((wheelDirection[ID] == true && commandInt == FORWARD) || 
       (wheelDirection[ID] == false && commandInt == BACKWARD)){
      //Art. FORWARD (Clockwise)
      command = (char)FORWARD_ART;
    }
    else if ((wheelDirection[ID] == true && commandInt == BACKWARD) || 
             (wheelDirection[ID] == false && commandInt == FORWARD)){
      //Art. Backward (Counter-Clockwise)
      command = (char)BACKWARD_ART;
    }
  }

  //adjust speed for corection factor
  int speed = (int)(tempSpeed*wheelCorectFactor[ID]);
  if(speed > 127){
    speed = 127;
  //  msg2user("Error: Motor #" + (String)(ID) + " has been given a speed greater than allowed, motor was slown down to it's max speed \n");
  }
  
  //checksum is an important variable/line of code for moving the motor
  unsigned char checksum = (address + command + ((char)speed)) & 0b01111111;
  
  // Write to the correct serial packet.
  if(wheelPinType[ID] == 1 || wheelPinType[ID] == 2){
    //This is the 4 lines of code that ACTUALY moves the motor, do not mess with
    Serial.write(address);
    Serial.write(command);
    Serial.write(((char)speed));
    Serial.write(checksum);
  }
  //so we don't overload any serial buffers
  delayMicroseconds(1500);
  //if we need to paused, paused
  //checkForInterupt(); // <-- May need this -------------------------------------------------------------------
}
