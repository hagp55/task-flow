import re


def camel_to_snake(name: str) -> str:
    """
    Convert a string from camel case to snake case.

    Args:
        name (str): The string in camel case format.

    Returns:
        str: The string converted to snake case format.
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def singular_to_plural(name: str) -> str:
    """
    Convert a word to its plural form.

    Args:
        name (str): The word to be converted to plural.

    Returns:
        str: The word in its plural form.
    """

    if name.endswith("y") and not name.endswith(("ay", "ey", "iy", "oy", "uy")):
        return name[:-1] + "ies"  # 'category' -> 'categories'
    if name.endswith(("s", "sh", "ch", "x", "z")):
        return name + "es"  # 'class' -> 'classes'
    return name + "s"  # 'user' -> 'users'
