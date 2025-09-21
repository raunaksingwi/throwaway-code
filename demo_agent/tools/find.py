"""find tool - search for text across files in the workspace."""

import os
import re
from pathlib import Path
from agents import function_tool
from ._shared import security_error_handler, is_valid_path


@function_tool(failure_error_function=security_error_handler)
def find(
    search_text: str,
    file_pattern: str = "**/*",
    case_sensitive: bool = True,
    whole_word: bool = False,
    max_results: int = 100,
    sort_by: str = "name"
) -> list[str]:
    """
    Search for text across files in the workspace.
    Args:
        search_text: The text to search for
        file_pattern: The file pattern to search in (defaults to all files)
        case_sensitive: Whether search should be case sensitive (default: True)
        whole_word: Whether to match whole words only (default: False)
        max_results: Maximum number of results to return (default: 100)
        sort_by: Sort method - "name", "mtime" (default: "name")
    Returns:
        A list of files containing the search text
    Raises:
        ValueError: If search_text is empty or invalid parameters
    """
    if not search_text:
        raise ValueError("No search text provided")

    # Validate parameters
    valid_sorts = ["name", "mtime"]
    if sort_by not in valid_sorts:
        raise ValueError(f"sort_by must be one of: {', '.join(valid_sorts)}")

    if max_results < 1:
        raise ValueError("max_results must be >= 1")

    workspace_root = os.getcwd()
    matches_with_info = []

    # Prepare search text based on options
    if whole_word:
        if case_sensitive:
            search_pattern = re.compile(r'\b' + re.escape(search_text) + r'\b')
        else:
            search_pattern = re.compile(r'\b' + re.escape(search_text) + r'\b', re.IGNORECASE)
    else:
        if not case_sensitive:
            search_text_lower = search_text.lower()

    # Normalize the file pattern for cross-platform compatibility
    file_pattern = os.path.normpath(file_pattern)

    # Use pathlib for recursive file search
    for file_path in Path(workspace_root).glob(file_pattern):
        if file_path.is_file():
            # Stop if we've reached max_results
            if len(matches_with_info) >= max_results:
                break

            # Validate the path is within workspace
            is_valid, _ = is_valid_path(str(file_path), workspace_root)
            if not is_valid:
                # Skip files outside workspace or ignored by .gitignore
                continue

            try:
                # Search for text in file
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    # Perform search based on options
                    found = False
                    if whole_word:
                        found = bool(search_pattern.search(content))
                    elif case_sensitive:
                        found = search_text in content
                    else:
                        found = search_text_lower in content.lower()

                    if found:
                        # Use os.path.relpath for cross-platform relative paths
                        rel_path = os.path.relpath(str(file_path), workspace_root)
                        stat_info = os.stat(file_path)
                        matches_with_info.append({
                            'path': rel_path,
                            'mtime': stat_info.st_mtime
                        })

            except (PermissionError, UnicodeDecodeError):
                # Skip unreadable files
                continue

    # Sort the matches
    if sort_by == "name":
        matches_with_info.sort(key=lambda x: x['path'].lower())
    elif sort_by == "mtime":
        matches_with_info.sort(key=lambda x: x['mtime'], reverse=True)

    # Return just the paths
    return [match['path'] for match in matches_with_info]