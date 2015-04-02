import math
import numpy
__author__ = 'Matt'

def drawWheelDisplay(canvas, x, y, size, data):

    wheelSize = size / 6

    drawWheel(canvas, x+size*1/4, y+size/6, wheelSize, data.frontLeftTheta, data.frontLeftSpeed, 0)
    drawWheel(canvas, x+size*1/4, y+size/6*3, wheelSize, data.frontLeftTheta, data.frontLeftSpeed, 0)
    drawWheel(canvas, x+size*1/4, y+size/6*5, wheelSize, data.frontLeftTheta, data.frontLeftSpeed, 0)

    drawWheel(canvas, x+size*3/4, y+size/6, wheelSize, data.frontLeftTheta, data.frontLeftSpeed, 0)
    drawWheel(canvas, x+size*3/4, y+size/6*3, wheelSize, data.frontLeftTheta, data.frontLeftSpeed, 0)
    drawWheel(canvas, x+size*3/4, y+size/6*5, wheelSize, data.frontLeftTheta, data.frontLeftSpeed, 0)


    return


def drawWheel(canvas, x, y, size, theta, speed, current):

    half_length = size/2

    rotationMatrix = numpy.matrix([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])


    rect = numpy.matrix(
        [[-half_length, -half_length],
         [-half_length, half_length],
         [half_length, half_length],
         [half_length, -half_length]]
    )

    speedArrow = numpy.matrix(
        [[half_length, 0],
         [half_length, half_length*speed]]
    )

    rotRect = rect.dot(rotationMatrix)
    rotSpeed = speedArrow.dot(rotationMatrix)


    canvas.create_polygon(
        x+rotRect[0].item(0), y+rotRect[0].item(1),
        x+rotRect[1].item(0), y+rotRect[1].item(1),
        x+rotRect[2].item(0), y+rotRect[2].item(1),
        x+rotRect[3].item(0), y+rotRect[3].item(1),
        fill="grey"
    )

    canvas.create_line(
        x+rotSpeed[0].item(0), y+rotSpeed[0].item(1),
        x+rotSpeed[1].item(0), y+rotSpeed[1].item(1),
        width=size/18,
        fill="purple"
    )

    return