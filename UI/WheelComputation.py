__author__ = 'Matt'

import cmath

# hard coded
FL_WHEEL_POS = (-1/6.0, -1/6.0)
ML_WHEEL_POS = (-1/6.0, 0.0)
RL_WHEEL_POS = (-1/6.0, 1/6.0)

FR_WHEEL_POS = (1/6.0, -1/6.0)
MR_WHEEL_POS = (1/6.0, 0.0)
RR_WHEEL_POS = (1/6.0, 1/6.0)


# TODO: Move away from using tangent
##
# Computes data for positioning the wheels
#
##
def wheelComp(wheelPos, arcCenter, goForward):

    adjacent = wheelPos[0]-arcCenter[0]
    tangent = 0

    if not goForward:
        if adjacent != 0:
            opposite = wheelPos[1]-arcCenter[1]

            tangent = opposite/float(adjacent)

    theta = cmath.atan(tangent) + cmath.pi/2

    theta = theta/cmath.pi*180

    return theta.real