"""Workspace tools exposed to OpenAI agents.

The helpers in this module provide the basic file-system tooling that aligns
with what "code interpreter" style agents expect.  Each tool is implemented as
an OpenAI Agents compatible callable so it can be plugged directly into an
agent configuration.

Tools implemented:
- ``pwd``: return the workspace root path.
- ``ls``: list directories/files relative to the workspace.
- ``glob``: resolve glob patterns.
- ``read_files``: stream the contents of one or more files.
- ``find``: search for text across the workspace.
- ``ast_grep``: search for AST patterns in code files using ast-grep.
- ``tree``: render directory tree structure.
"""

# Import all tools
from .pwd import pwd
from .ls import ls
from .glob import glob
from .ast_grep import ast_grep
from .read_files import read_files
from .find import find
from .tree import tree

# Export all tools
__all__ = [
    "pwd",
    "ls",
    "glob",
    "read_files",
    "find",
    "ast_grep",
    "tree",
]