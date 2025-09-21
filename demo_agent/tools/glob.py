"""glob tool - resolve glob patterns within the workspace."""

import os
import glob as glob_module
from agents import function_tool
from ._shared import security_error_handler, is_valid_path


@function_tool(failure_error_function=security_error_handler)
def glob(
    pattern: str,
    sort_by: str = "name",
    max_results: int = 1000,
    reverse: bool = False
) -> list[str]:
    """
    Resolve glob patterns within the workspace.
    Args:
        pattern: The glob pattern to resolve.
        sort_by: Sort method - "name", "mtime", "size" (default: "name")
        max_results: Maximum number of results to return (default: 1000)
        reverse: Reverse the sort order (default: False)
    Returns:
        A list of files that match the glob pattern.
    """
    if not pattern:
        raise ValueError("No pattern provided")

    # Validate sort_by parameter
    valid_sorts = ["name", "mtime", "size"]
    if sort_by not in valid_sorts:
        raise ValueError(f"sort_by must be one of: {', '.join(valid_sorts)}")

    if max_results < 1:
        raise ValueError("max_results must be >= 1")

    # Get all matching files
    matches = glob_module.glob(pattern)

    # Filter out any matches that are outside the current working directory or ignored
    workspace_root = os.getcwd()
    valid_matches_with_info = []

    for match in matches:
        is_valid, _ = is_valid_path(match, workspace_root)
        if is_valid:
            try:
                stat_info = os.stat(match)
                valid_matches_with_info.append({
                    'path': match,
                    'mtime': stat_info.st_mtime,
                    'size': stat_info.st_size
                })
            except (OSError, PermissionError):
                # Include files we can't stat
                valid_matches_with_info.append({
                    'path': match,
                    'mtime': 0,
                    'size': 0
                })

    # Sort the matches
    if sort_by == "name":
        valid_matches_with_info.sort(key=lambda x: x['path'].lower())
    elif sort_by == "mtime":
        valid_matches_with_info.sort(key=lambda x: x['mtime'])
    elif sort_by == "size":
        valid_matches_with_info.sort(key=lambda x: x['size'])

    if reverse:
        valid_matches_with_info.reverse()

    # Apply max_results limit and return just the paths
    limited_matches = valid_matches_with_info[:max_results]
    return [match['path'] for match in limited_matches]