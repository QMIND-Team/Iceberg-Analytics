import math


def angleCalc(x, y):
    if y == 0:
        y = 0.0001
    if x == -2650:
        x = -2650.0001
    if y > 0:
        return 45 + math.degrees(math.atan((x + 2650) / y))
    elif (x + 2650) > 0:
        return 135 - math.degrees(math.atan(y / (x + 2650)))
    else:
        return 225 + math.degrees(math.atan((x + 2650) / y))
