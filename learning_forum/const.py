"""
    Defines Constants used in Forum application
"""

# time
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

# color
COLOR_PINK = "#f56c6c"
COLOR_BROWN = "#e6a23c"
COLOR_GREEN = "#5cb87a"
COLOR_BLUE = "#1989fa"
COLOR_PURPLE = "#6f7ad3"

# status
STATUS_TODO = 1
STATUS_ACTIVE = 2
STATUS_COMPLETE = 3

# comments
COMMENT_STATUS_ACTIVE = 1   # comments can be display
COMMENT_STATUS_BANNED = 2   # comments force deleted by admin
COMMENT_STATUS_DELETE = 3   # comments deleted by user who commented

# comments
POST_STATUS_PUBLIC = 1   # posts published in public
POST_STATUS_PRIVATE = 2  # posts published in private
POST_STATUS_BANNED = 3   # posts force deleted by admin
POST_STATUS_DELETE = 4   # posts deleted by user who commented
