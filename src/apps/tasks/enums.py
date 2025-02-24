from enum import Enum


class Priority(str, Enum):
    """
    This class represents the priority of a task.

    Attributes:
        low (str): The low priority.
        medium (str): The medium priority.
        high (str): The high priority.
    """

    low = "low"
    medium = "medium"
    high = "high"


class Status(str, Enum):
    """
    This class represents the status of a task.

    Attributes:
        progress (str): The task is in progress.
        pending (str): The task is pending.
        completed (str): The task is completed.
    """

    pending = "pending"
    progress = "progress"
    completed = "completed"
