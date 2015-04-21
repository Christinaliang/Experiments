__author__ = 'Matt'

import math
import cmath
from UI.network.DataTransferProtocol import sendData
import UI.WheelComputation as WheelComputation
from MathHelpers import *
import numpy

class DriveControl:

    def __init__(self, x, y, size, data, data_client):
        self.x = x
        self.y = y

        self.size = size
        self.path_area_size = self.size - self.size/self.SIDE_BOX_RATIO
        self.half_size = self.path_area_size/2

        self.robot_center_radius = self.path_area_size/self.ROBOT_DOT_RADIUS_RATIO
        self.path_dot_radius = self.path_area_size/self.PATH_DOT_RADIUS_RATIO

        # A Rectangle defining two corners of the path area on the UI
        self.path_area = (x, y+self.path_area_size/self.SIDE_BOX_RATIO, x+size, y+size)

        # Where the robot is centered on the UI
        self.robot_center = (self.path_area[0]+self.half_size, self.path_area[1]+self.half_size)

        self.throttle_center = (x+self.path_area_size, y + size/self.SIDE_BOX_RATIO + self.half_size)

        self.current_control = self.NO_AREA_SELECTED

        self.ui_data = data

        self.dataClient = data_client

        self.button_active = True
        self.radius_offset_x = 0
        self.radius_offset_y = 0
        self.go_forward = True
        # 0 is stop, -100 is full reverse, 100 is full forward
        self.throttle = 0

        self.fl_pos = (WheelComputation.FL_WHEEL_POS[0],
                       WheelComputation.FL_WHEEL_POS[1])

        self.fr_pos = (WheelComputation.FR_WHEEL_POS[0],
                       WheelComputation.FR_WHEEL_POS[1])

        self.ml_pos = (WheelComputation.ML_WHEEL_POS[0],
                       WheelComputation.ML_WHEEL_POS[1])

        self.mr_pos = (WheelComputation.MR_WHEEL_POS[0],
                       WheelComputation.MR_WHEEL_POS[1])

        self.rl_pos = (WheelComputation.RL_WHEEL_POS[0],
                       WheelComputation.RL_WHEEL_POS[1])

        self.rr_pos = (WheelComputation.RR_WHEEL_POS[0],
                       WheelComputation.RR_WHEEL_POS[1])

        self.wheel_matrix = WheelComputation.WHEEL_MATRIX

        return

    NO_AREA_SELECTED = -1
    PATH_AREA_SELECTED = 0
    THROTTLE_AREA_SELECTED = 1
    ACTIVATE_AREA_SELECTED = 2

    SCALE = 1

    SIDE_BOX_RATIO = 18

    ROBOT_DOT_RADIUS_RATIO = 75
    PATH_DOT_RADIUS_RATIO = 150
    WHEEL_DOT_RADIUS_RATIO = 300

    def draw(self, canvas):

        arc_center = (self.robot_center[0] + self.radius_offset_x, self.robot_center[1] + self.radius_offset_y)

        # Draw the snap to objects
        canvas.create_line(self.x, self.robot_center[1], self.x+self.path_area_size, self.robot_center[1], fill="grey")
        canvas.create_oval(self.robot_center[0]-self.robot_center_radius,
                           self.robot_center[1]-self.robot_center_radius,
                           self.robot_center[0]+self.robot_center_radius,
                           self.robot_center[1]+self.robot_center_radius, fill="grey")

        # Draw the wheels
        self.draw_wheel2(canvas, (self.robot_center[0]+self.fl_pos[0], self.robot_center[1]+self.fl_pos[1]),
                        arc_center,
                        self.path_area_size, self.ui_data.fl_articulation_angle)
        self.draw_wheel2(canvas, (self.robot_center[0]+self.ml_pos[0], self.robot_center[1]+self.ml_pos[1]),
                        arc_center, self.path_area_size, self.ui_data.ml_articulation_angle)
        self.draw_wheel2(canvas, (self.robot_center[0]+self.rl_pos[0], self.robot_center[1]+self.rl_pos[1]),
                        arc_center,
                        self.path_area_size, self.ui_data.rl_articulation_angle)
        self.draw_wheel2(canvas, (self.robot_center[0]+self.fr_pos[0], self.robot_center[1]+self.fr_pos[1]),
                        arc_center,
                        self.path_area_size, self.ui_data.fr_articulation_angle)
        self.draw_wheel2(canvas, (self.robot_center[0]+self.mr_pos[0], self.robot_center[1]+self.mr_pos[1]),
                        arc_center,
                        self.path_area_size, self.ui_data.mr_articulation_angle)
        self.draw_wheel2(canvas, (self.robot_center[0]+self.rr_pos[0], self.robot_center[1]+self.rr_pos[1]),
                        arc_center,
                        self.path_area_size, self.ui_data.rr_articulation_angle)

        # Draw
        if self.go_forward:
            canvas.create_rectangle(self.x, self.y, self.path_area_size, self.path_area_size/self.SIDE_BOX_RATIO,
                                    fill="purple")
            # canvas.create_oval(arcCenter[0]-self.pathDotRadius, arcCenter[1]-self.pathDotRadius,
            #                    arcCenter[0]+self.pathDotRadius, arcCenter[1]+self.pathDotRadius,
            #                    fill="grey")
        else:
            canvas.create_rectangle(self.x, self.y, self.path_area_size, self.path_area_size/self.SIDE_BOX_RATIO,
                                    fill="grey")
            canvas.create_oval(arc_center[0]-self.path_dot_radius, arc_center[1]-self.path_dot_radius,
                               arc_center[0]+self.path_dot_radius, arc_center[1]+self.path_dot_radius,
                               fill="black")

        self.draw_path(canvas, arc_center)

        # Draw throttle area

        throttle_left = self.x+self.path_area_size
        throttle_right = self.x+self.size

        canvas.create_rectangle(throttle_left, self.y+self.size/self.SIDE_BOX_RATIO,
                                throttle_right, self.y+self.size,
                                fill="grey")

        throttle_top = self.throttle_center[1]-2
        throttle_bottom = self.throttle_center[1]+2

        if self.throttle > 0:
            throttle_top = self.throttle_center[1] + self.half_size * self.throttle/-100
        elif self.throttle < 0:
            throttle_bottom = self.throttle_center[1] + self.half_size*self.throttle/-100

        canvas.create_rectangle(throttle_left, throttle_top, throttle_right, throttle_bottom, fill="purple")

        # Draw Activate Area
        if not self.button_active:
            active_color = "red"
        else:
            active_color = "green"
        canvas.create_rectangle(self.x+self.path_area_size, self.y,
                                self.x+self.size, self.y+self.size/self.SIDE_BOX_RATIO,
                                fill=active_color)

        return

    def draw_path(self, canvas, arc_center):

        # Driving forward
        if self.go_forward:

            path_end_pos = self.y+self.size/self.SIDE_BOX_RATIO+self.half_size+self.half_size*self.throttle/-100

            canvas.create_line(self.robot_center[0], self.y+self.size/self.SIDE_BOX_RATIO,
                               self.x+self.path_area_size/2, self.y+self.size)
            canvas.create_line(self.robot_center[0], self.y+self.size/self.SIDE_BOX_RATIO+self.half_size,
                               self.x+self.path_area_size/2, path_end_pos,
                               fill="purple", width=2)

            canvas.create_oval(self.robot_center[0]-self.path_dot_radius, path_end_pos-self.path_dot_radius,
                               self.robot_center[0]+self.path_dot_radius, path_end_pos+self.path_dot_radius,
                               fill="purple")

            # canvas.create_oval(arcCenter[0]-self.arcCenterRadius, arcCenter[1]-self.arcCenterRadius,
            # arcCenter[0]+self.arcCenterRadius, arcCenter[1]+self.arcCenterRadius,
            # fill="grey")

        # Rotation
        elif self.robot_center[0] == arc_center[0] and self.robot_center[1] == arc_center[1]:
            radius = self.half_size/4

            arc_degree_length = float(359)*self.throttle/100

            canvas.create_oval(arc_center[0]-radius, arc_center[1]-radius,
                               arc_center[0]+radius, arc_center[1]+radius,
                               fill=None)
            canvas.create_arc(arc_center[0]-radius, arc_center[1]-radius,
                              arc_center[0]+radius, arc_center[1]+radius,
                              fill=None, style="arc", outline="purple", width=2,
                              start=90, extent=arc_degree_length)

            path_end_pos_x = arc_center[0]+cmath.cos((arc_degree_length+90)/180*cmath.pi.real).real*radius
            path_end_pos_y = arc_center[1]+cmath.sin((arc_degree_length+90)/180*cmath.pi.real).real*radius*-1

            canvas.create_oval(path_end_pos_x-self.path_dot_radius, path_end_pos_y-self.path_dot_radius,
                               path_end_pos_x+self.path_dot_radius, path_end_pos_y+self.path_dot_radius,
                               fill="purple")

        # Arcing
        else:

            # Compute the radius of the arc
            radius = dist(arc_center[0], arc_center[1], self.robot_center[0], self.robot_center[1])

            # Draw the circle that the arc falls on
            canvas.create_oval(arc_center[0]-radius, arc_center[1]-radius,
                               arc_center[0]+radius, arc_center[1]+radius,
                               fill=None)

            theta = 0.0

            # Adjacent is the length of line adjacent to theta
            # Hypotenuse is our radius
            # Theta is the interior angle around the point of rotation

            # Top Right Quadrant
            if arc_center[0] > self.robot_center[0] and arc_center[1] <= self.robot_center[1]:
                adjacent = arc_center[0] - self.robot_center[0]
                theta = 180 + (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real
            # Top Left Quadrant
            if arc_center[0] < self.robot_center[0] and arc_center[1] < self.robot_center[1]:
                adjacent = self.robot_center[0] - arc_center[0]
                theta = 360 - (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real
            # Bottom Left Quadrant
            if arc_center[0] < self.robot_center[0] and arc_center[1] > self.robot_center[1]:
                adjacent = self.robot_center[1] - arc_center[1]
                theta = (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real-90
            # Bottom Right Quadrant
            if arc_center[0] > self.robot_center[0] and arc_center[1] > self.robot_center[1]:
                adjacent = arc_center[1] - self.robot_center[1]
                theta = (cmath.acos(float(adjacent)/float(radius)).real/cmath.pi.real*180).real+90

            # We want forward throttle to always move the robot forward. This enforces that behavior
            if arc_center[0] > self.robot_center[0]:
                throttlePathMod = -1
                arc_degree_length = 360 - (float(359)*self.throttle/100 - theta)
            else:
                throttlePathMod = 1
                arc_degree_length = 360 - (float(359)*self.throttle/100*-1 - theta)
            # The purple arc to represent actual drive distance around the circle
            canvas.create_arc(arc_center[0]-radius, arc_center[1]-radius, arc_center[0]+radius, arc_center[1]+radius,
                              start=theta, extent=359*self.throttle/100*throttlePathMod,
                              fill=None, style="arc", outline="purple", width=2)

            # The position that the robot will stop at, the end of the arc
            path_end_pos_x = arc_center[0]+cmath.cos(deg2rad(arc_degree_length)).real*radius
            path_end_pos_y = arc_center[1]+cmath.sin(deg2rad(arc_degree_length)).real*radius*-1

            # Draw a marker to show the position that the robot will stop at
            canvas.create_oval(path_end_pos_x-self.path_dot_radius,
                               path_end_pos_y-self.path_dot_radius,
                               path_end_pos_x+self.path_dot_radius,
                               path_end_pos_y+self.path_dot_radius,
                               fill="purple")

        return

    def draw_wheel(self, canvas, wheel_pos, arc_center_pos, size, theta):

        # Radius of the dot to draw at the wheel
        wheel_dot_radius = size/self.WHEEL_DOT_RADIUS_RATIO

        # Draw a dot at the center of the wheel
        canvas.create_oval(wheel_pos[0]-wheel_dot_radius, wheel_pos[1]-wheel_dot_radius,
                           wheel_pos[0]+wheel_dot_radius, wheel_pos[1]+wheel_dot_radius,
                           fill="black")

        # Created a dotted line from the wheel to the center of the circle it will be driving around
        if not self.go_forward:
            canvas.create_line(wheel_pos[0], wheel_pos[1],
                               arc_center_pos[0], arc_center_pos[1],
                               dash=(1, 1))

        dx = size/self.WHEEL_LENGTH_RATIO*cmath.cos(deg2rad(theta)).real
        dy = size/self.WHEEL_LENGTH_RATIO*cmath.sin(deg2rad(theta)).real

        # Draw the wheel line
        canvas.create_line(wheel_pos[0]-dx, wheel_pos[1]-dy,
                           wheel_pos[0]+dx, wheel_pos[1]+dy,
                           width=size/self.WHEEL_WIDTH_RATIO)

        return


    def draw_wheel2(self, canvas, wheel_pos, arc_center_pos, size, theta):

        # theta = theta + 90
        rot = numpy.matrix(
            [[math.cos(deg2rad(theta)), -math.sin(deg2rad(theta))],
            [math.sin(deg2rad(theta)), math.cos(deg2rad(theta))]]
        )

        rotated = self.wheel_matrix.dot(rot)

        canvas.create_polygon(wheel_pos[0]+rotated[0].item(0), wheel_pos[1]+rotated[0].item(1),
                              wheel_pos[0]+rotated[1].item(0), wheel_pos[1]+rotated[1].item(1),
                              wheel_pos[0]+rotated[2].item(0), wheel_pos[1]+rotated[2].item(1),
                              wheel_pos[0]+rotated[3].item(0), wheel_pos[1]+rotated[3].item(1),
                              wheel_pos[0]+rotated[4].item(0), wheel_pos[1]+rotated[4].item(1),
                              wheel_pos[0]+rotated[5].item(0), wheel_pos[1]+rotated[5].item(1),
                              wheel_pos[0]+rotated[6].item(0), wheel_pos[1]+rotated[6].item(1),
                              wheel_pos[0]+rotated[7].item(0), wheel_pos[1]+rotated[7].item(1))

        # Created a dotted line from the wheel to the center of the circle it will be driving around
        if not self.go_forward:
            canvas.create_line(wheel_pos[0], wheel_pos[1],
                               arc_center_pos[0], arc_center_pos[1],
                               dash=(1, 1))


        # Draw a dot at the center of the wheel
        canvas.create_oval(wheel_pos[0]-2, wheel_pos[1]-2,
                           wheel_pos[0]+2, wheel_pos[1]+2,
                           fill="grey", outline=None)

        return

    def on_mouse_press(self, event):

        # Mark which area the user first clicked in
        if event.x < self.x + self.path_area_size:
            self.current_control = self.PATH_AREA_SELECTED
        elif event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO:
            self.current_control = self.ACTIVATE_AREA_SELECTED
        else:
            self.current_control = self.THROTTLE_AREA_SELECTED

        return

    # Users should never ever call this.
    def on_mouse_motion(self, event):

        # If the user first clicked in the path definition area
        if self.current_control == self.PATH_AREA_SELECTED:
            # if the cursor is in the top box area, set the wheels to go forward mode
            self.go_forward = event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO

            # If we are going forward then all wheels should be pointing in this direction
            if self.go_forward:
                self.ui_data.fl_articulation_angle = 180
                self.ui_data.fr_articulation_angle = 0
                self.ui_data.ml_articulation_angle = 180
                self.ui_data.mr_articulation_angle = 0
                self.ui_data.rl_articulation_angle = 180
                self.ui_data.rr_articulation_angle = 0
                return

            # If the cursor leaves the path definition area then don't do anything
            if event.x > self.x + self.path_area_size:
                return

            # If the user gets close enough to the robot center point then snap to the robot center
            if dist(event.x, event.y, self.robot_center[0], self.robot_center[1]) < self.path_area_size/self.ROBOT_DOT_RADIUS_RATIO:
                self.radius_offset_x = 0
                self.radius_offset_y = 0

            # If the user gets close enough to the center (horizontal) line, then snap to it
            elif dist(0, event.y, 0, self.robot_center[1]) < self.size/75:
                self.radius_offset_x = event.x - self.robot_center[0]
                self.radius_offset_y = 0

            # Otherwise we just use the coordinates of the cursor
            else:
                self.radius_offset_x = event.x - self.robot_center[0]
                self.radius_offset_y = event.y - self.robot_center[1]

            arc_center_pos = (self.radius_offset_x, self.radius_offset_y)

            # Compute the angle and speed of each of the articulation joints/wheels
            self.ui_data.fl_articulation_angle = 360 - WheelComputation.calc_articulation_angle(self.fl_pos, arc_center_pos, self.go_forward) + 180
            self.ui_data.fl_drive_speed = WheelComputation.calc_wheel_speed(self.fl_pos, arc_center_pos, self.go_forward)

            self.ui_data.fr_articulation_angle = 360 - WheelComputation.calc_articulation_angle(self.fr_pos, arc_center_pos, self.go_forward)
            self.ui_data.fr_drive_speed = WheelComputation.calc_wheel_speed(self.fr_pos, arc_center_pos, self.go_forward)

            self.ui_data.ml_articulation_angle = 360 - WheelComputation.calc_articulation_angle(self.ml_pos, arc_center_pos, self.go_forward) + 180
            self.ui_data.ml_drive_speed = WheelComputation.calc_wheel_speed(self.ml_pos, arc_center_pos, self.go_forward)

            self.ui_data.mr_articulation_angle = 360 - WheelComputation.calc_articulation_angle(self.mr_pos, arc_center_pos, self.go_forward)
            self.ui_data.mr_drive_speed = WheelComputation.calc_wheel_speed(self.mr_pos, arc_center_pos, self.go_forward)

            self.ui_data.rl_articulation_angle = 360 - WheelComputation.calc_articulation_angle(self.rl_pos, arc_center_pos, self.go_forward) + 180
            self.ui_data.rl_drive_speed = WheelComputation.calc_wheel_speed(self.rl_pos, arc_center_pos, self.go_forward)

            self.ui_data.rr_articulation_angle = 360 - WheelComputation.calc_articulation_angle(self.rr_pos, arc_center_pos, self.go_forward)
            self.ui_data.rr_drive_speed = WheelComputation.calc_wheel_speed(self.rr_pos, arc_center_pos, self.go_forward)

            # Normalize all speeds to that they are between 0 and 1
            WheelComputation.normalize_wheel_speeds(self.ui_data)

        # If the user first clicked in the throttle area
        if self.current_control == self.THROTTLE_AREA_SELECTED:

            # If the user moves the cursor out of the throttle area then don't do anything
            if event.y > self.size or event.y < self.size/self.SIDE_BOX_RATIO:
                return

            # Compute the throttle value
            self.throttle = (self.throttle_center[1] - event.y)*100/self.half_size

        return

    def on_mouse_release(self, event):

        # If the user is releasing the mouse in the activate area and they first clicked in the activate area then
        #   send a command to the robot
        #   activate the button
        if event.x > self.x + self.path_area_size and event.y < self.y+self.path_area_size/self.SIDE_BOX_RATIO:
            if self.current_control == self.ACTIVATE_AREA_SELECTED:

                if self.button_active:
                    self.button_active = False
                    sendData(self.dataClient.socket, self.ui_data)

                else:
                    self.button_active = True

                    self.ui_data.e_stop = True
                    sendData(self.dataClient.socket, self.ui_data)
                    self.ui_data.e_stop = False

        self.current_control = self.NO_AREA_SELECTED
        return

