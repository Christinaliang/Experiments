__author__ = 'Matt'

import cmath


def dist(x1, y1, x2, y2):
    dx = x1-x2
    dy = y1-y2

    return cmath.sqrt(dx*dx + dy*dy).real


def rad2deg(theta):
    return theta/cmath.pi.real*180.0


def deg2rad(theta):
    return theta*cmath.pi.real/180.0
