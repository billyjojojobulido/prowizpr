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

# posts publish
POST_PUBLISH_STATUS_PUBLIC = 1   # posts published in public
POST_PUBLISH_STATUS_PRIVATE = 2  # posts published in private

# posts status
POST_STATUS_ACTIVE = 1      # posts are active
POST_STATUS_BANNED = 0      # posts are banned by admin

# like
LIKE_LIKE = 1
LIKE_DISLIKE = 0
LIKE_TYPE_POST = 1       # like a post
LIKE_TYPE_COMMENT = 2    # like a comment

# user
USER_IS_ADMIN = 1
USER_NOT_ADMIN = 0
USER_ACCOUNT_ACTIVE = True
USER_ACCOUNT_BANNED = False
