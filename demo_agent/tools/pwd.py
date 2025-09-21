"""pwd tool - return the workspace root path."""

import os
from agents import function_tool
from ._shared import security_error_handler


@function_tool(failure_error_function=security_error_handler)
def pwd() -> str:
    """
    Return the workspace root path.
    Returns:
        The workspace root path.
    """
    return os.getcwd()