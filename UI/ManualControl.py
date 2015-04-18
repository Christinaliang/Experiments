__author__ = 'Matt'

import math
import cmath
from UI.network.DataTransferProtocol import sendData
import UI.WheelComputation as WheelCompuation


class DriveControl:

    def __init__(self, x, y, size, data, dataClient):
        self.x = x
        self.y = y

        self.size = size
        self.path_area_size = self.size - self.size/self.SIDE_BOX_RATIO
        self.half_size = self.path_area_size/2

        self.robotCenterRadius = self.path_area_size/self.ROBOT_DOT_RADIUS_RATIO
        self.pathDotRadius = self.path_area_size/self.PATH_DOT_RADIUS_RATIO

        # A Rectangle defining two corners of the path area on the UI
        self.path_area = (x, y+self.path_area_size/self.SIDE_BOX_RATIO, x+size, y+size)

        # Where the robot is centered on the UI
        self.robotCenter = (self.path_area[0]+self.half_size, self.path_area[1]+self.half_size)

        self.throttleCenter = (x+self.path_area_size, y + size/self.SIDE_BOX_RATIO + self.half_size)

        self.currentControl = self.NO_AREA_SELECTED

        self.uiData = data

        self.dataClient = dataClient

        self.button_active = True
        self.radius_offset_x = 0
        self.radius_offset_y = 0
        self.go_forward = True
        # 0 is stop, -100 is full reverse, 100 is full forward
        self.throttle = 0



        self.fl_pos = (self.path_area_size*WheelCompuation.FL_WHEEL_POS[0]*self.SCALE,
                  self.path_area_size*WheelCompuation.FL_WHEEL_POS[1]*self.SCALE)

        self.fr_pos = (self.path_area_size*WheelCompuation.FR_WHEEL_POS[0]*self.SCALE,
                  self.path_area_size*WheelCompuation.FR_WHEEL_POS[1]*self.SCALE)

        self.ml_pos = (self.path_area_size*WheelCompuation.ML_WHEEL_POS[0]*self.SCALE,
                  self.path_area_size*WheelCompuation.ML_WHEEL_POS[1]*self.SCALE)

        self.mr_pos = (self.path_area_size*WheelCompuation.MR_WHEEL_POS[0]*self.SCALE,
                  self.path_area_size*WheelCompuation.MR_WHEEL_POS[1]*self.SCALE)

        self.rl_pos = (self.path_area_size*WheelCompuation.RL_WHEEL_POS[0]*self.SCALE,
                  self.path_area_size*WheelCompuation.RL_WHEEL_POS[1]*self.SCALE)

        self.rr_pos = (self.path_area_size*WheelCompuation.RR_WHEEL_POS[0]*self.SCALE,
                  self.path_area_size*WheelCompuation.RR_WHEEL_POS[1]*self.SCALE)

        return


    NO_AREA_SELECTED = -1
    PATH_AREA_SELECTED = 0
    THROTTLE_AREA_SELECTED = 1
    ACTIVATE_AREA_SELECTED = 2

    SCALE = 1/3.0

    SIDE_BOX_RATIO = 18

    WHEEL_LENGTH_RATIO = 25/SCALE
    WHEEL_WIDTH_RATIO = 50/SCALE

    WHEEL_GAP_X_RATIO = 6/SCALE
    WHEEL_GAP_Y_RATIO = 6/SCALE

    ROBOT_DOT_RADIUS_RATIO = 25/SCALE
    PATH_DOT_RADIUS_RATIO = 50/SCALE
    WHEEL_DOT_RADIUS_RATIO = 100/SCALE

    def draw(self, canvas):

        arcCenter = (self.robotCenter[0] + self.radius_offset_x, self.robotCenter[1] + self.radius_offset_y)


        # Draw the snap to objects
        canvas.create_line(self.x, self.robotCenter[1], self.x+self.path_area_size, self.robotCenter[1], fill="grey")
        canvas.create_oval(self.robotCenter[0]-self.robotCenterRadius,
                           self.robotCenter[1]-self.robotCenterRadius,
                           self.robotCenter[0]+self.robotCenterRadius,
                           self.robotCenter[1]+self.robotCenterRadius, fill="grey")

        # Draw the wheels
        self.drawWheel(canvas, (self.robotCenter[0]+self.fl_pos[0], self.robotCenter[1]+self.fl_pos[1]), arcCenter, self.path_area_size, self.uiData.fl_articulation_angle)
        self.drawWheel(canvas, (self.robotCenter[0]+self.ml_pos[0], self.robotCenter[1]+self.ml_pos[1]), arcCenter, self.path_area_size, self.uiData.ml_articulation_angle)
        self.drawWheel(canvas, (self.robotCenter[0]+self.rl_pos[0], self.robotCenter[1]+self.rl_pos[1]), arcCenter, self.path_area_size, self.uiData.rl_articulation_angle)
        self.drawWheel(canvas, (self.robotCenter[0]+self.fr_pos[0], self.robotCenter[1]+self.fr_pos[1]), arcCenter, self.path_area_size, self.uiData.fr_articulation_angle)
        self.drawWheel(canvas, (self.robotCenter[0]+self.mr_pos[0], self.robotCenter[1]+self.mr_pos[1]), arcCenter, self.path_area_size, self.uiData.mr_articulation_angle)
        self.drawWheel(canvas, (self.robotCenter[0]+self.rr_pos[0], self.robotCenter[1]+self.rr_pos[1]), arcCenter, self.path_area_size, self.uiData.rr_articulation_angle)

        # Draw
        if self.go_forward:
            canvas.create_rectangle((self.x, self.y, self.path_area_size, self.path_area_size/self.SIDE_BOX_RATIO), fill="purple")
            canvas.create_oval(arcCenter[0]-self.pathDotRadius, arcCenter[1]-self.pathDotRadius, arcCenter[0]+self.pathDotRadius, arcCenter[1]+self.pathDotRadius, fill="grey")
        else:
            canvas.create_rectangle((self.x, self.y, self.path_area_size, self.path_area_size/self.SIDE_BOX_RATIO), fill="grey")
            canvas.create_oval(arcCenter[0]-self.pathDotRadius, arcCenter[1]-self.pathDotRadius, arcCenter[0]+self.pathDotRadius, arcCenter[1]+self.pathDotRadius, fill="purple")


        self.drawPath(canvas, arcCenter)

        # Draw throttle area

        throttleLeft = self.x+self.path_area_size
        throttleRight = self.x+self.size

        canvas.create_rectangle(throttleLeft, self.y+self.size/self.SIDE_BOX_RATIO, throttleRight, self.y+self.size, fill="grey")

        throttleTop = self.throttleCenter[1]-2
        throttleBottom = self.throttleCenter[1]+2

        if self.throttle > 0:
            throttleTop = self.throttleCenter[1] + self.half_size * self.throttle/-100
        elif self.throttle < 0:
            throttleBottom = self.throttleCenter[1] + self.half_size*self.throttle/-100

        canvas.create_rectangle(throttleLeft, throttleTop, throttleRight, throttleBottom, fill="purple")

        # Draw Activate Area
        ActiveColor = "green"
        if self.button_active == False:
            ActiveColor = "red"
        canvas.create_rectangle(self.x+self.path_area_size, self.y, self.x+self.size, self.y+self.size/self.SIDE_BOX_RATIO, fill=ActiveColor)

        return

    def drawPath(self, canvas, arcCenter):

        # Driving forward
        if self.go_forward:

            pathEndPos = self.y+self.size/self.SIDE_BOX_RATIO+self.half_size+self.half_size*self.throttle/-100

            canvas.create_line(self.robotCenter[0], self.y+self.size/self.SIDE_BOX_RATIO, self.x+self.path_area_size/2, self.y+self.size)
            canvas.create_line(self.robotCenter[0],
                               self.y+self.size/self.SIDE_BOX_RATIO+self.half_size,
                               self.x+self.path_area_size/2,
                               pathEndPos,
                               fill="purple", width=2)

            canvas.create_oval(self.robotCenter[0]-self.pathDotRadius,
                               pathEndPos-self.pathDotRadius,
                               self.robotCenter[0]+self.pathDotRadius,
                               pathEndPos+self.pathDotRadius,
                               fill="purple")

            # canvas.create_oval(arcCenter[0]-self.arcCenterRadius, arcCenter[1]-self.arcCenterRadius, arcCenter[0]+self.arcCenterRadius, arcCenter[1]+self.arcCenterRadius, fill="grey")

        # Rotation
        elif self.robotCenter[0] == arcCenter[0] and self.robotCenter[1] == arcCenter[1]:
            radius = self.half_size/4

            arcDegreeLength = float(359)*self.throttle/100

            canvas.create_oval(arcCenter[0]-radius, arcCenter[1]-radius, arcCenter[0]+radius, arcCenter[1]+radius, fill=None)
            canvas.create_arc(arcCenter[0]-radius, arcCenter[1]-radius, arcCenter[0]+radius, arcCenter[1]+radius, fill=None, style="arc", outline="purple", width=2, start=90, extent=arcDegreeLength)

            pathEndPos_x = arcCenter[0]+cmath.cos((arcDegreeLength+90)/180*cmath.pi.real).real*radius
            pathEndPos_y = arcCenter[1]+cmath.sin((arcDegreeLength+90)/180*cmath.pi.real).real*radius*-1

            canvas.create_oval(pathEndPos_x-self.pathDotRadius,
                               pathEndPos_y-self.pathDotRadius,
                               pathEndPos_x+self.pathDotRadius,
                               pathEndPos_y+self.pathDotRadius,
                               fill="purple")

        # Arcing
        else:

            # Compute the radius of the arc
            radius = dist(arcCenter[0], arcCenter[1], self.robotCenter[0], self.robotCenter[1])

            # Draw the circle that the arc falls on
            canvas.create_oval(arcCenter[0]-radius, arcCenter[1]-radius, arcCenter[0]+radius, arcCenter[1]+radius, fill=None)

            theta = 0.0

            # Adjacent is the length of line adjacent to theta
            # Hypotenuse is our radius
            # Theta is the interior angle around the point of rotation

            # Top Right Quadrant
            if arcCenter[0] > self.robotCenter[0] and arcCenter[1] <= self.robotCenter[1]:
                adjacent = arcCenter[0] - self.robotCenter[0]
                theta = 180 + (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real
            # Top Left Quadrant
            if arcCenter[0] < self.robotCenter[0] and arcCenter[1] < self.robotCenter[1]:
                adjacent = self.robotCenter[0] - arcCenter[0]
                theta = 360 -(cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real
            # Bottom Left Quadrant
            if arcCenter[0] < self.robotCenter[0] and arcCenter[1] > self.robotCenter[1]:
                adjacent = self.robotCenter[1] - arcCenter[1]
                theta = (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real-90
            # Bottom Right Quadrant
            if arcCenter[0] > self.robotCenter[0] and arcCenter[1] > self.robotCenter[1]:
                adjacent = arcCenter[1] - self.robotCenter[1]
                theta = (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real+90

            # We want forward throttle to always move the robot forward. This enforces that behavior
            if arcCenter[0] > self.robotCenter[0]:
                throttlePathMod = -1
                arcDegreeLength = 360 - (float(359)*self.throttle/100 - theta)
            else:
                throttlePathMod = 1
                arcDegreeLength = 360 - (float(359)*self.throttle/100*-1 - theta)
            # The purple arc to represent actual drive distance around the circle
            canvas.create_arc(arcCenter[0]-radius, arcCenter[1]-radius, arcCenter[0]+radius, arcCenter[1]+radius,
                              start=theta, extent=359*self.throttle/100*throttlePathMod,
                              fill=None, style="arc", outline="purple", width=2)

            # The position that the robot will stop at, the end of the arc
            pathEndPos_x = arcCenter[0]+cmath.cos(deg2rad(arcDegreeLength)).real*radius
            pathEndPos_y = arcCenter[1]+cmath.sin(deg2rad(arcDegreeLength)).real*radius*-1

            # Draw a marker to show the position that the robot will stop at
            canvas.create_oval(pathEndPos_x-self.pathDotRadius,
                               pathEndPos_y-self.pathDotRadius,
                               pathEndPos_x+self.pathDotRadius,
                               pathEndPos_y+self.pathDotRadius,
                               fill="purple")

        return

    def drawWheel(self, canvas, wheelPos, arcCenterPos, size, theta):

        # Radius of the dot to draw at the wheel
        wheelDotRadius = size/self.WHEEL_DOT_RADIUS_RATIO

        # Draw a dot at the center of the wheel
        canvas.create_oval(wheelPos[0]-wheelDotRadius, wheelPos[1]-wheelDotRadius, wheelPos[0]+wheelDotRadius, wheelPos[1]+wheelDotRadius, fill="black")

        # Created a dotted line from the wheel to the center of the circle it will be driving around
        if not self.go_forward:
            canvas.create_line(wheelPos[0], wheelPos[1], arcCenterPos[0], arcCenterPos[1], dash=(1, 1))

        dX = size/self.WHEEL_LENGTH_RATIO*cmath.cos(deg2rad(theta)).real
        dY = size/self.WHEEL_LENGTH_RATIO*cmath.sin(deg2rad(theta)).real

        # Draw the wheel line
        canvas.create_line(wheelPos[0]-dX, wheelPos[1]-dY, wheelPos[0]+dX, wheelPos[1]+dY, width=size/self.WHEEL_WIDTH_RATIO)

        return

    def onMousePress(self, event):

        # Mark which area the user first clicked in
        if event.x < self.x + self.path_area_size:
            self.currentControl = self.PATH_AREA_SELECTED
        elif event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO:
            self.currentControl = self.ACTIVATE_AREA_SELECTED
        else:
            self.currentControl = self.THROTTLE_AREA_SELECTED

        return

    # Users should never ever call this.
    def onMouseMotion(self, event):

        # If the user first clicked in the path definition area
        if self.currentControl == self.PATH_AREA_SELECTED:
            # if the cursor is in the top box area, set the wheels to go forward mode
            self.go_forward = event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO

            # If we are going forward then all wheels should be pointing in this direction
            if self.go_forward:
                self.uiData.fl_articulation_angle = 90
                self.uiData.fr_articulation_angle = 90
                self.uiData.ml_articulation_angle = 90
                self.uiData.mr_articulation_angle = 90
                self.uiData.rl_articulation_angle = 90
                self.uiData.rr_articulation_angle = 90
                return

            # If the cursor leaves the path definition area then don't do anything
            if event.x > self.x + self.path_area_size:
                return

            # If the user gets close enough to the robot center point then snap to the robot center
            if dist(event.x, event.y, self.robotCenter[0], self.robotCenter[1]) < self.path_area_size/self.ROBOT_DOT_RADIUS_RATIO:
                self.radius_offset_x = 0
                self.radius_offset_y = 0

            # If the user gets close enough to the center (horizontal) line, then snap to it
            elif dist(0, event.y, 0, self.robotCenter[1]) < self.size/75:
                self.radius_offset_x = event.x - self.robotCenter[0]
                self.radius_offset_y = 0

            # Otherwise we just use the coordinates of the cursor
            else:
                self.radius_offset_x = event.x - self.robotCenter[0]
                self.radius_offset_y = event.y - self.robotCenter[1]

            arcCenterPos = (self.radius_offset_x, self.radius_offset_y)

            # Compute the angle of each of the articulation joints
            self.uiData.fl_articulation_angle = WheelCompuation.wheelComp(self.fl_pos, arcCenterPos, self.go_forward)
            self.uiData.fr_articulation_angle = WheelCompuation.wheelComp(self.fr_pos, arcCenterPos, self.go_forward)
            self.uiData.ml_articulation_angle = WheelCompuation.wheelComp(self.ml_pos, arcCenterPos, self.go_forward)
            self.uiData.mr_articulation_angle = WheelCompuation.wheelComp(self.mr_pos, arcCenterPos, self.go_forward)
            self.uiData.rl_articulation_angle = WheelCompuation.wheelComp(self.rl_pos, arcCenterPos, self.go_forward)
            self.uiData.rr_articulation_angle = WheelCompuation.wheelComp(self.rr_pos, arcCenterPos, self.go_forward)

        # If the user first clicked in the throttle area
        if self.currentControl == self.THROTTLE_AREA_SELECTED:

            # If the user moves the cursor out of the throttle area then don't do anything
            if event.y > self.size or event.y < self.size/self.SIDE_BOX_RATIO:
                return

            # Compute the throttle value
            self.throttle = (self.throttleCenter[1] - event.y)*100/self.half_size

        return

    def onMouseRelease(self, event):

        # If the user is releasing the mouse in the activate area and they first clicked in the activate area then
        #   send a command to the robot
        #   activate the button
        if event.x > self.x + self.path_area_size and event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO:
            if self.currentControl == self.ACTIVATE_AREA_SELECTED:

                self.button_active = False
                sendData(self.dataClient.socket, self.uiData)

        self.currentControl = self.NO_AREA_SELECTED
        return


def dist(x1, y1, x2, y2):
    dX = x1-x2
    dY = y1-y2

    return cmath.sqrt(dX*dX + dY*dY).real


def rad2deg(theta):
    return theta/cmath.pi.real*180.0


def deg2rad(theta):
    return theta*cmath.pi.real/180.0