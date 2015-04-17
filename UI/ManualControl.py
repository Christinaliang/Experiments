__author__ = 'Matt'

import cmath
from UI.network.DataTransferProtocol import sendData


class DriveControl:

    def __init__(self, x, y, size, data, dataClient):
        self.x = x
        self.y = y

        self.size = size
        self.path_area_size = self.size - self.size/self.SIDE_BOX_RATIO
        self.half_size = self.path_area_size/2

        # A Rectangle defining two corners of the path area on the UI
        self.path_area = (x, y+self.path_area_size/self.SIDE_BOX_RATIO, x+size, y+size)

        # Where the robot is centered on the UI
        self.robotCenter = (self.path_area[0]+self.half_size, self.path_area[1]+self.half_size)

        self.throttleCenter = (x+self.path_area_size, y + size/self.SIDE_BOX_RATIO + self.half_size)

        self.currentControl = self.NO_AREA_SELECTED

        self.uiData = data

        self.dataCient = dataClient

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
    ARC_DOT_RADIUS_RATIO = 50/SCALE
    WHEEL_DOT_RADIUS_RATIO = 100/SCALE

    def draw(self, canvas):

        arcCenter = (self.robotCenter[0] + self.uiData.radius_offset_x, self.robotCenter[1] + self.uiData.radius_offset_y)

        robotCenterRadius= self.path_area_size/self.ROBOT_DOT_RADIUS_RATIO
        arcCenterRadius = self.path_area_size/self.ARC_DOT_RADIUS_RATIO

        # Draw the snap to objects
        canvas.create_line(self.x, self.robotCenter[1], self.x+self.path_area_size, self.robotCenter[1], fill="grey")
        canvas.create_oval(self.robotCenter[0]-robotCenterRadius,
                           self.robotCenter[1]-robotCenterRadius,
                           self.robotCenter[0]+robotCenterRadius,
                           self.robotCenter[1]+robotCenterRadius, fill="grey")

        # Draw the wheels
        wheelXOffset = self.path_area_size/self.WHEEL_GAP_X_RATIO
        wheelYOffset = self.path_area_size/self.WHEEL_GAP_Y_RATIO
        self.drawWheel(canvas, (self.robotCenter[0]-wheelXOffset, self.robotCenter[1]-wheelYOffset),   arcCenter, self.path_area_size, self.uiData)
        self.drawWheel(canvas, (self.robotCenter[0]-wheelXOffset, self.robotCenter[1]),                arcCenter, self.path_area_size, self.uiData)
        self.drawWheel(canvas, (self.robotCenter[0]-wheelXOffset, self.robotCenter[1]+wheelYOffset),   arcCenter, self.path_area_size, self.uiData)
        self.drawWheel(canvas, (self.robotCenter[0]+wheelXOffset, self.robotCenter[1]-wheelYOffset),   arcCenter, self.path_area_size, self.uiData)
        self.drawWheel(canvas, (self.robotCenter[0]+wheelXOffset, self.robotCenter[1]),                arcCenter, self.path_area_size, self.uiData)
        self.drawWheel(canvas, (self.robotCenter[0]+wheelXOffset, self.robotCenter[1]+wheelYOffset),   arcCenter, self.path_area_size, self.uiData)

        if self.uiData.go_forward:

            canvas.create_line(self.robotCenter[0], self.y+self.size/self.SIDE_BOX_RATIO, self.x+self.path_area_size/2, self.y+self.size)
            canvas.create_line(self.robotCenter[0],
                               self.y+self.size/self.SIDE_BOX_RATIO+self.half_size,
                               self.x+self.path_area_size/2,
                               self.y+self.size/self.SIDE_BOX_RATIO+self.half_size+self.half_size*self.uiData.throttle/-100,
                               fill="purple", width=2)

            canvas.create_rectangle((self.x, self.y, self.path_area_size, self.path_area_size/self.SIDE_BOX_RATIO), fill="purple")
            canvas.create_oval(arcCenter[0]-arcCenterRadius, arcCenter[1]-arcCenterRadius, arcCenter[0]+arcCenterRadius, arcCenter[1]+arcCenterRadius, fill="grey")
        else:

            radius = dist(arcCenter[0], arcCenter[1], self.robotCenter[0], self.robotCenter[1])
            canvas.create_oval(arcCenter[0]-radius, arcCenter[1]-radius, arcCenter[0]+radius, arcCenter[1]+radius, fill=None)

            theta = 0.0

            x1 = arcCenter[0]
            y1 = arcCenter[1]

            x2 = self.robotCenter[0]
            y2 = self.robotCenter[1]

            throttlePathMod = 1

            # Top Right Quadrant
            if x1 > x2 and y1 <= y2:
                adjacent = x1 - x2
                theta = 180 + (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real
            # Top Left Quadrant
            if x1 < x2 and y1 < y2:
                adjacent = x2 - x1
                theta = 360 -(cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real
            # Bottom Left Quadrant
            if x1 < x2 and y1 > y2:
                adjacent = y2 - y1
                theta = (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real-90
            # Bottom Right Quadrant
            if x1 > x2 and y1 > y2:
                adjacent = y1 - y2
                theta = (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real+90

            if x1 > x2:
                throttlePathMod = -1

            canvas.create_arc(arcCenter[0]-radius, arcCenter[1]-radius, arcCenter[0]+radius, arcCenter[1]+radius, fill=None, style="arc", outline="purple", width=2, start=theta, extent=359*self.uiData.throttle/100*throttlePathMod)


            canvas.create_rectangle((self.x, self.y, self.path_area_size, self.path_area_size/self.SIDE_BOX_RATIO), fill="grey")
            canvas.create_oval(arcCenter[0]-arcCenterRadius, arcCenter[1]-arcCenterRadius, arcCenter[0]+arcCenterRadius, arcCenter[1]+arcCenterRadius, fill="purple")

        # Draw throttle area

        throttleLeft = self.x+self.path_area_size
        throttleRight = self.x+self.size

        canvas.create_rectangle(throttleLeft, self.y+self.size/self.SIDE_BOX_RATIO, throttleRight, self.y+self.size, fill="grey")

        throttleTop = self.throttleCenter[1]-2
        throttleBottom = self.throttleCenter[1]+2

        if self.uiData.throttle > 0:
            throttleTop = self.throttleCenter[1] + self.half_size * self.uiData.throttle/-100
        elif self.uiData.throttle < 0:
            throttleBottom = self.throttleCenter[1] + self.half_size*self.uiData.throttle/-100

        canvas.create_rectangle(throttleLeft, throttleTop, throttleRight, throttleBottom, fill="purple")

        # Draw Activate Area
        canvas.create_rectangle(self.x+self.path_area_size, self.y, self.x+self.size, self.y+self.size/self.SIDE_BOX_RATIO, fill="green")

        return

    def drawWheel(self, canvas, wheelPos, arcCenterPos, size, manualControlData):

        wheelDotRadius = size/self.WHEEL_DOT_RADIUS_RATIO

        canvas.create_oval(wheelPos[0]-wheelDotRadius, wheelPos[1]-wheelDotRadius, wheelPos[0]+wheelDotRadius, wheelPos[1]+wheelDotRadius, fill="black")

        adjacent = wheelPos[0]-arcCenterPos[0]
        tangent = 0

        if not manualControlData.go_forward:
            canvas.create_line(wheelPos[0], wheelPos[1], arcCenterPos[0], arcCenterPos[1], dash=(1, 1))
            if adjacent != 0:
                opposite = wheelPos[1]-arcCenterPos[1]
                tangent = opposite/float(adjacent)

        theta = cmath.atan(tangent) + cmath.pi/2

        dX = size/self.WHEEL_LENGTH_RATIO*cmath.cos(theta).real
        dY = size/self.WHEEL_LENGTH_RATIO*cmath.sin(theta).real

        canvas.create_line(wheelPos[0]-dX, wheelPos[1]-dY, wheelPos[0]+dX, wheelPos[1]+dY, width=size/self.WHEEL_WIDTH_RATIO)

        return

    def onMousePress(self, event):

        if event.x < self.x + self.path_area_size:
            self.currentControl = self.PATH_AREA_SELECTED
        elif event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO:
            self.currentControl = self.ACTIVATE_AREA_SELECTED
        else:
            self.currentControl = self.THROTTLE_AREA_SELECTED

        return

    def onMouseMotion(self, event):

        # print str(event.x) + "," + str(event.y)

        if self.currentControl == self.PATH_AREA_SELECTED:
            self.uiData.go_forward = event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO

            if event.x > self.x + self.path_area_size:
                return

            if dist(event.x, event.y, self.robotCenter[0], self.robotCenter[1]) < self.path_area_size/self.ROBOT_DOT_RADIUS_RATIO:
                self.uiData.radius_offset_x = 0
                self.uiData.radius_offset_y = 0
            elif dist(0, event.y, 0, self.robotCenter[1]) < self.size/75:
                self.uiData.radius_offset_x = event.x - self.robotCenter[0]
                self.uiData.radius_offset_y = 0
            else:
                self.uiData.radius_offset_x = event.x - self.robotCenter[0]
                self.uiData.radius_offset_y = event.y - self.robotCenter[1]

        if self.currentControl == self.THROTTLE_AREA_SELECTED:

            if event.y > self.size or event.y < self.size/self.SIDE_BOX_RATIO:
                return

            self.uiData.throttle = (self.throttleCenter[1] - event.y)*100/self.half_size
            return

        return

    def onMouseRelease(self, event):

        if event.x > self.x + self.path_area_size and event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO:
            if self.currentControl == self.ACTIVATE_AREA_SELECTED:

                sendData(self.dataCient.socket, self.uiData)

                return

        self.currentControl = self.NO_AREA_SELECTED
        return


def dist(x1, y1, x2, y2):
    dX = x1-x2
    dY = y1-y2

    return cmath.sqrt(dX*dX + dY*dY).real