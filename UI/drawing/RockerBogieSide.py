__author__ = 'Matt'

import math
import numpy

def drawRockerBogie(canvas, x, y, size, armData, flip):

    HORIZONTAL_SHIFT = size/2
    VERTICAL_SHIFT = size/3

    bogieTheta = armData.bogieTheta
    rockerTheta = armData.rockerTheta


    shortArmLength = size/6
    longArmLength = size/3
    width = size/100

    # Inner arm
    bogieMatrix = numpy.matrix(
        [[-shortArmLength, 0],
         [shortArmLength, 0]]
    )

    bogieRotation = numpy.matrix(
        [[math.cos(bogieTheta), -math.sin(bogieTheta)],
         [math.sin(bogieTheta), math.cos(bogieTheta)]]
    )

    bogieShift = numpy.matrix(
        [[-shortArmLength, shortArmLength],
         [-shortArmLength, shortArmLength]]
    )


    bogieMatrix = bogieMatrix.dot(bogieRotation)
    bogieMatrix = bogieMatrix + bogieShift


    # Outer arm
    rockerMatrix = numpy.matrix(
        [[-shortArmLength, shortArmLength],
         [0, 0],
         [longArmLength, shortArmLength]]

    )

    rockerRotation = numpy.matrix(
        [[math.cos(rockerTheta), -math.sin(rockerTheta)],
         [math.sin(rockerTheta), math.cos(rockerTheta)]]
    )

    rockerMatrix = rockerMatrix.dot(rockerRotation)
    bogieMatrix = bogieMatrix.dot(rockerRotation)


    if flip:
        flipMatrix = numpy.matrix(
            [[-1, 0],
             [0, 1]]
        )

        rockerMatrix = rockerMatrix.dot(flipMatrix)
        bogieMatrix = bogieMatrix.dot(flipMatrix)

    canvas.create_line(
        x+bogieMatrix[0].item(0)+HORIZONTAL_SHIFT, y+bogieMatrix[0].item(1)+VERTICAL_SHIFT,
        x+bogieMatrix[1].item(0)+HORIZONTAL_SHIFT, y+bogieMatrix[1].item(1)+VERTICAL_SHIFT,\
        width=width,
        fill="purple"
    )

    canvas.create_line(
        x+rockerMatrix[0].item(0)+HORIZONTAL_SHIFT, y+rockerMatrix[0].item(1)+VERTICAL_SHIFT,
        x+rockerMatrix[1].item(0)+HORIZONTAL_SHIFT, y+rockerMatrix[1].item(1)+VERTICAL_SHIFT,
        x+rockerMatrix[2].item(0)+HORIZONTAL_SHIFT, y+rockerMatrix[2].item(1)+VERTICAL_SHIFT,
        width=width,
        fill="purple"
    )


    return