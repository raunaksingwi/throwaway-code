"""Shared utilities and imports for demo_agent tools."""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Any, List

import pathspec
from agents import RunContextWrapper

logger = logging.getLogger(__name__)


def security_error_handler(context: RunContextWrapper[Any], error: Exception) -> str:
    """
    Custom error handler for file system tools.

    Provides informative error messages to the LLM when it encounters errors.

    Args:
        context: The run context wrapper
        error: The exception that occurred

    Returns:
        A user-friendly error message for the LLM
    """
    # Parameters are required by the error handler interface but not used in this implementation
    return (
        f"Error: I encountered an error while trying to access a file or directory. "
        f"For security reasons, I can only access files within the current workspace directory "
        f"({os.getcwd()}). Please ensure the path you're requesting is within this directory."
    )


# Filesystem utilities (formerly from utils/fs.py)

def parse_gitignore(gitignore_path: str) -> pathspec.PathSpec:
    """Load patterns from a ``.gitignore`` file and return a PathSpec."""

    patterns: list[str] = []
    try:
        with open(gitignore_path, "r", encoding="utf-8") as file_obj:
            for line in file_obj:
                cleaned = line.strip()
                if cleaned and not cleaned.startswith("#"):
                    patterns.append(cleaned)
    except (FileNotFoundError, UnicodeDecodeError):
        pass

    # Create PathSpec from patterns using gitwildmatch for gitignore compatibility
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)


def find_gitignore_files(workspace_root: str) -> List[str]:
    """Return all ``.gitignore`` files within the workspace tree."""

    discovered: list[str] = []
    try:
        for root, _dirs, files in os.walk(workspace_root):
            if ".gitignore" in files:
                discovered.append(os.path.join(root, ".gitignore"))
    except (PermissionError, OSError):
        pass
    return discovered


def should_ignore_path(path: str, workspace_root: str) -> bool:
    """Determine whether ``path`` should be ignored based on gitignore rules."""

    try:
        rel_path = os.path.relpath(path, workspace_root)
    except ValueError:
        return True

    if rel_path == ".":
        return False
    if rel_path == ".git" or rel_path.startswith(".git" + os.sep):
        return True

    # Normalize path separators for cross-platform compatibility
    rel_path = rel_path.replace(os.sep, '/')

    for gitignore_file in find_gitignore_files(workspace_root):
        pathspec_obj = parse_gitignore(gitignore_file)
        gitignore_dir = os.path.dirname(gitignore_file)

        try:
            rel_from_gitignore = os.path.relpath(path, gitignore_dir)
        except ValueError:
            continue

        if rel_from_gitignore == os.pardir or rel_from_gitignore.startswith(os.pardir + os.sep):
            continue

        # Normalize path separators for pathspec
        rel_from_gitignore = rel_from_gitignore.replace(os.sep, '/')

        # Check if the path matches any pattern in this gitignore
        if pathspec_obj.match_file(rel_from_gitignore):
            return True

    return False


def is_valid_path(path: str, base_path: str | None = None, check_gitignore: bool = True) -> tuple[bool, str | None]:
    """Check if path resides inside base_path and is not ignored.

    Args:
        path: The path to validate
        base_path: The base directory (defaults to current workspace)
        check_gitignore: Whether to check gitignore patterns

    Returns:
        Tuple of (is_valid, resolved_path). If valid, resolved_path contains
        the absolute path. If invalid, resolved_path is None.
    """
    base_path = base_path or os.getcwd()

    try:
        path = os.path.normpath(path)
        base_path = os.path.normpath(base_path)

        abs_base = Path(base_path).resolve()
        abs_path = Path(path).resolve()

        # Check if path is within base_path
        abs_path.relative_to(abs_base)

        # Check gitignore patterns if requested
        if check_gitignore and should_ignore_path(str(abs_path), base_path):
            return False, None

        return True, str(abs_path)

    except (ValueError, OSError):
        return False, None