"""tree tool - render directory tree structure."""

import os
from pathlib import Path
from agents import function_tool
from directory_tree import display_tree as directory_display_tree
from ._shared import security_error_handler, is_valid_path, logger


@function_tool(failure_error_function=security_error_handler)
def tree(
    path: str = ".",
    *,
    max_depth: int = 2,
    include_files: bool = True,
    max_entries: int = 200,
) -> str:
    """Render a directory tree rooted at ``path`` using ``directory_tree``.

    Args:
        path: Directory to render; defaults to the current workspace root.
        max_depth: Maximum depth (>=1) to traverse. Depth counts directories.
        include_files: Whether to include files in the output (default True).
        max_entries: Maximum number of items to render before truncating.

    Returns:
        A string containing an ASCII tree representation of the directory.

    Raises:
        ValueError: If ``max_depth`` or ``max_entries`` are < 1 or not integers.
        NotADirectoryError: If ``path`` is not a directory.
        FileNotFoundError: If ``path`` does not exist.
    """

    try:
        max_depth = int(max_depth)
    except (TypeError, ValueError):
        raise ValueError("max_depth must be an integer >= 1") from None
    if max_depth < 1:
        raise ValueError("max_depth must be an integer >= 1")

    try:
        max_entries = int(max_entries)
    except (TypeError, ValueError):
        raise ValueError("max_entries must be an integer >= 1") from None
    if max_entries < 1:
        raise ValueError("max_entries must be an integer >= 1")

    workspace_root = os.getcwd()
    is_valid, validated_path_str = is_valid_path(path)
    if not is_valid:
        raise FileNotFoundError(f"Path '{path}' does not exist or is not accessible")
    validated_path = Path(validated_path_str)
    if not validated_path.exists():
        raise FileNotFoundError(f"Path '{path}' does not exist")
    if not validated_path.is_dir():
        raise NotADirectoryError(f"Path '{path}' is not a directory")

    root_label = path if path not in ("", ".") else Path(workspace_root).name
    root_label = (root_label or validated_path.name) + "/"

    only_dirs = not include_files

    try:
        rendered = directory_display_tree(
            dir_path=str(validated_path),
            string_rep=True,
            header=False,
            max_depth=max_depth,
            show_hidden=False,
            ignore_list=None,
            only_files=False,
            only_dirs=only_dirs,
            sort_by=0,
            raise_exception=True,
            print_error_traceback=False,
        )
    except Exception as err:
        logger.warning("Failed to render tree for %s: %s", validated_path, err)
        raise

    if rendered is None:
        rendered = ""

    rendered_lines = [root_label.rstrip("/") + "/"]
    entries_added = 0

    for line in rendered.splitlines():
        if not line.strip():
            continue
        rendered_lines.append(line)
        entries_added += 1
        if entries_added >= max_entries:
            rendered_lines.append("└── …")
            break

    return "\n".join(rendered_lines)