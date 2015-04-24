How to run the robot. As of (4/23/2015)

Robot Setup
1. Invite Matt Holland to come play with robots
2. SSH on to the master pi on the robot. (pi5 at time of writing)
3. (optional, highly recommended) My preference is to use tmux to have all commands running simultaneously in their own
    pane, otherwise you can probably just append a '&' to every command to make them all run in the same window
    tmux cheatsheet: https://gist.github.com/MohamedAlaa/2961058
4. run the command "roscore"
5. run the command "sudo chmod 777 /dev/ttyACM*"
6. run the command "rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0" <or other port>
7. run the command "rosrun command2ros RobotDataServer.py"
8. (optional) run the command "rostopic echo /ManualCommand" to view commands from the UI to the motor driving system
9. (optional) run the command "rostopic echo /testing" to view debug print stuff

Client Setup
1. Invite Matt Holland to come play with robots
2. Go to your client machine and open your UI workspace in PyCharm (or whatever way you want to do it)
3. Open UI/network/RobotDataClient.py and change the ip address to that of the server

To Open the GUI
4. run UI/runClientGui.py

To send a manual command
4. Open the file UI/ManualControl.py
5. edit values to your hearts content
6. Run UI/ManualControl.py