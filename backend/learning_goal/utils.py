import time
import learning_goal.const as const


# time_format() format the time value to
def time_format(t):
    ret = t.strftime(const.TIME_FORMAT)
    return ret


def date_format(t):
    ret = t.strftime(const.DATE_FORMAT)
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


# check_str_empty() check if the input string is empty: None or ""
def check_str_empty(param):
    if param is None or len(param) == 0:
        return True
    return False


# get_full_name() generate the full name of the user
def get_full_name(first_name, last_name):
    if not check_str_empty(first_name) and not check_str_empty(last_name):
        return "{} {}".format(first_name, last_name)
    elif not check_str_empty(first_name) and check_str_empty(last_name):
        return first_name
    elif check_str_empty(first_name) and not check_str_empty(last_name):
        return last_name
    else:
        return "Unnamed User"


# get_progress_msg() generate the string msg based on the progress int
def get_progress_msg(status):
    if status == const.STATUS_TODO:
        return "To Do"
    if status == const.STATUS_ACTIVE:
        return "In Progress"
    if status == const.STATUS_COMPLETE:
        return "Done"
    return "Invalid Task Progress"

def get_publish_msg(publish_status):
    if publish_status == const.STATUS_PUBLISH:
        return "Publish"
    if publish_status == const.STATUS_PRIVATE:
        return "Private"
    return "Invalid publish status"
