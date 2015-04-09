import math
import numpy
__author__ = 'Matt'


def drawWheelDisplay(canvas, x, y, size, data):

    wheelSize = size / 6

    drawWheel(canvas, x+size*1/4, y+size/6, wheelSize, data.frontLeftWheel)
    drawWheel(canvas, x+size*1/4, y+size/6*3, wheelSize, data.midLeftWheel)
    drawWheel(canvas, x+size*1/4, y+size/6*5, wheelSize, data.rearLeftWheel)

    drawWheel(canvas, x+size*3/4, y+size/6, wheelSize, data.frontRightWheel)
    drawWheel(canvas, x+size*3/4, y+size/6*3, wheelSize, data.midRightWheel)
    drawWheel(canvas, x+size*3/4, y+size/6*5, wheelSize, data.midRightWheel)


##
# drawWheel
#
# Description - draws a wheel with position, rotation, and indicators based on given data
#
def drawWheel(canvas, x, y, size, wheelData):

    half_length = size/2

    # Some fun linear algebra to rotate the wheel
    rotationMatrix = numpy.matrix(
        [[math.cos(wheelData.theta), -math.sin(wheelData.theta)],
         [math.sin(wheelData.theta), math.cos(wheelData.theta)]]
    )

    rect = numpy.matrix(
        [[-half_length, -half_length],
         [-half_length, half_length],
         [half_length, half_length],
         [half_length, -half_length]]
    )

    speedArrow = numpy.matrix(
        [[half_length, 0],
         [half_length, half_length*wheelData.speed]]
    )

    rotRect = rect.dot(rotationMatrix)
    rotSpeed = speedArrow.dot(rotationMatrix)
    # end of fun linear algebra

    # Draw the wheel
    canvas.create_polygon(
        x+rotRect[0].item(0), y+rotRect[0].item(1),
        x+rotRect[1].item(0), y+rotRect[1].item(1),
        x+rotRect[2].item(0), y+rotRect[2].item(1),
        x+rotRect[3].item(0), y+rotRect[3].item(1),
        fill="grey"
    )

    # Draw the speed intensity bar
    canvas.create_line(
        x+rotSpeed[0].item(0), y+rotSpeed[0].item(1),
        x+rotSpeed[1].item(0), y+rotSpeed[1].item(1),
        width=size/18,
        fill="purple"
    )

    return