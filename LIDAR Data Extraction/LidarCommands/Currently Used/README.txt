Hello again! Alex Schendel here.
These are all the code files we are using to control the Lidar. Note, all this code will only run on a Raspberry Pi!
constants.py - A file where we define constants, such as array index values, Lidar resolution, and all the servo motor control constants.
lidar_servo_driver.py - A file to control the servo motor. This uses PWM to control the motor. The frequency and pin as well as min and max vals are defined in constants.
raspi_threads.py - Double thread file to produce and process data from the Lidar. This is the file that will actually be run. It uses the other files as supports for this purpose
utility.py - Essentially support functions for processing Lidar data

UPDATE:
lidar_servo_driver.py is not controlling the servo motor properly. It will be used to relay messages to Arduino?
Use an Arduino running lidar_servo_driver.ino (inside the lidar_servo_driver directory)