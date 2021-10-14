import time
import learning_forum.const as const


# time_format() format the time value to
def time_format(t):
    ret = t.strftime(const.TIME_FORMAT)
    return ret


# get_color() return the color with reference to the percentage
def get_color(percentage):
    # ensure percentage is in the range 0 - 1
    if percentage < 0:
        percentage = 0
    elif percentage > 100:
        percentage = 100

    # assigning color
    if percentage < 20:
        return const.COLOR_PINK
    elif percentage < 40:
        return const.COLOR_BROWN
    elif percentage < 60:
        return const.COLOR_GREEN
    elif percentage < 80:
        return const.COLOR_BLUE
    elif percentage <= 100:
        return const.COLOR_PURPLE

