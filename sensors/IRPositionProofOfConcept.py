import math


#Field Size Constants (centimeters):
LUNARENA_WIDTH = 378
LUNARENA_HEIGHT = 738


##
# Description: Generates a list of position sensor values [FORE, PORT, AFT, STARBOARD]
# based on the three-tuple (X,Y,ORIENTATION).
#
# (0,0) is "bottom left" of the arena, if you start at the bottom.
# (378, 738) is the "top right" of the arena.
#
# Note that our current IR sensors are valid for values from 15-150.
#   (TODO: Not implemented yet. Currently using Perfect Information until we have an algorithm.)
# Orientation:
#
# Parameters:
#       The tuple (x,y,orientation), where:
#           x: X-value (in cm, from "bottom left" of the arena).
#           y: Y-value (in cm, from "bottom left" of the arena).
#           orientation: degrees. 0 degrees is EAST (math coordinates). Valid inputs are 0 - 360.
#
# Returns:
#       A list of position sensor values: [fore, port, aft, starboard].
#
def generateIRValuesFromPosition(position):
    # Convert the tuple into friendlier, more descriptive variables.
    x = position[0]
    y = position[1]
    angleDeg = position[2]
    effectiveAngleDeg = angleDeg

    # For now, pretend that the robot can only face from 0 to 90 degrees. Later, we'll use rotational symmetry to
    # compensate for the actual orientation of the device.
    if 90 <= effectiveAngleDeg:
        effectiveAngleDeg %= 90

    # Special Case: If the angle is 0 or a multiple of 90, the problem is trivial.
    fore = LUNARENA_WIDTH - x
    aft = x
    port = LUNARENA_HEIGHT - y
    starboard = y

    # Otherwise, we must beseech the Law of Sines to determine simulated sensor values.
    if 0 != effectiveAngleDeg:
        # We need the angle in radians for python trigonometry.
        angleRadians = math.radians(effectiveAngleDeg)

        # These are some values we'll use over and over and over with the Law of Sines: A/Sin(a) [*Sin(90)] = B
        sinRadians = math.sin(angleRadians)
        sinHalfPiMinusRadians = math.sin(math.pi / 2 - angleRadians)

        # The "forward" sensor can only face the EAST or NORTH walls of the LunArena.
        foreEAST = (LUNARENA_WIDTH - x) / sinHalfPiMinusRadians
        foreNORTH = (LUNARENA_HEIGHT - y) / sinRadians
        # We choose the smaller of these values (the ray that gets cut off by a wall first).
        fore = min(foreNORTH, foreEAST)

        # The "port" sensor can only face the NORTH or WEST walls of the LunArena.
        portNORTH = (LUNARENA_HEIGHT - y) / sinHalfPiMinusRadians
        portWEST = x / sinRadians
        # We choose the smaller of these values (the ray that gets cut off by a wall first).
        port = min(portNORTH, portWEST)

        # The "aft" sensor can only face the WEST or SOUTH walls of the LunArena.
        aftWEST = x / sinHalfPiMinusRadians
        aftSOUTH = y / sinRadians
        # We choose the smaller of these values (the ray that gets cut off by a wall first).
        aft = min(aftWEST, aftSOUTH)

        #The "starboard" sensor can only face the SOUTH or EAST walls of the LunArena.
        starSOUTH = y / sinHalfPiMinusRadians
        starEAST = (LUNARENA_WIDTH - x) / sinRadians
        # We choose the smaller of these values (the ray that gets cut off by a wall first).
        starboard = min(starSOUTH, starEAST)

    # Build the list to return.
    retval = [fore, port, aft, starboard]
    # Compensate for starting angles larger than 90 degrees by "rotating" the sensor values.
    while 90 >= angleDeg:
        angleDeg -= 90
        # Take the first sensor value and move it to the end of the list
        # (rotate sensors "right": Forward goes to Starboard, Port goes to Forward, etc).
        retval.append(retval.pop(0))

    # We're done!
    return retval


# This will be a draft of the Position Fusion Sensor, suitable for testing  autonomous functions.
# For now, this function can assume that the device is on the "near" half of the field (the half the robot starts on).
# This will eventually have to be replaced with non-LunArena-wall-based systems, but for now this is fine.
def estimatePositionFromIRSensors(fore, port, aft, starboard):
    #TODO: Implement this.
    return


# Test that rotations work as intended.
p1 = generateIRValuesFromPosition((0, 0, 0))
assert([378, 738, 0, 0] == p1)
p1 = generateIRValuesFromPosition((0, 0, 90))
assert([738, 0, 0, 378] == p1)
p1 = generateIRValuesFromPosition((0, 0, 180))
assert([0, 0, 378, 738] == p1)
p1 = generateIRValuesFromPosition((0, 0, 270))
assert([0, 378, 738, 0] == p1)