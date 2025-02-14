class UserNotFoundException(Exception):
    detail: str = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail: str = "User not correct password"
