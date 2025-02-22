class UserNotFoundException(Exception):
    detail: str = "User not found"


class UserAlreadyExistsException(Exception):
    detail: str = "User with this email already exists"


class UserNotCorrectPasswordException(Exception):
    detail: str = "User not correct password"


class TokenExpiredException(Exception):
    detail: str = "Token has expired"


class TokenHasNotValidSignatureException(Exception):
    detail: str = "Token has not valid signature"


class TaskNotFoundException(Exception):
    detail: str = "Task not found"
