class UserNotFoundException(Exception):
    detail: str = "User not found"


class UserAlreadyExistsException(Exception):
    detail: str = "User already exists"


class UserNotCorrectPasswordException(Exception):
    detail: str = "User not correct password"


class TokenExpiredException(Exception):
    detail: str = "Token has expired"


class TokenHasNotValidSignatureException(Exception):
    detail: str = "Token has not valid signature"


class TaskNotFoundException(Exception):
    detail: str = "Task not found"


class TaskAlreadyExistsException(Exception):
    detail: str = "Task already exists"


class ProjectNotFoundException(Exception):
    detail: str = "Project not found"


class ProjectAlreadyExistsException(Exception):
    detail: str = "Project already exists"


class PermissionDeniedException(Exception):
    detail: str = "Token has not valid signature"
