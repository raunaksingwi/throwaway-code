"""ls tool - list directories/files relative to the workspace."""

import os
import time
from agents import function_tool
from ._shared import is_valid_path


@function_tool()
def ls(
    path: str = ".",
    sort_by: str = "name",
    show_hidden: bool = False,
    show_details: bool = False,
    reverse: bool = False
) -> list[str] | str:
    """
    List directories/files relative to the workspace.
    Args:
        path: The directory path to list (defaults to current directory)
        sort_by: Sort method - "name", "mtime", "size", "type" (default: "name")
        show_hidden: Include hidden files/directories (default: False)
        show_details: Return detailed information as string (default: False)
        reverse: Reverse the sort order (default: False)
    Returns:
        A list of directories/files, or detailed string if show_details=True
    """
    # Validate sort_by parameter
    valid_sorts = ["name", "mtime", "size", "type"]
    if sort_by not in valid_sorts:
        raise ValueError(f"sort_by must be one of: {', '.join(valid_sorts)}")

    is_valid, validated_path = is_valid_path(path)
    if not is_valid:
        return [] if not show_details else f"Invalid path: {path}"

    workspace_root = os.getcwd()

    # Get all items in the directory with their metadata
    items_with_info = []
    try:
        all_items = os.listdir(validated_path)

        for item in all_items:
            # Skip hidden files unless requested
            if not show_hidden and item.startswith('.'):
                continue

            item_path = os.path.join(validated_path, item)
            is_item_valid, _ = is_valid_path(item_path, workspace_root)
            if is_item_valid:
                try:
                    stat_info = os.stat(item_path)
                    is_dir = os.path.isdir(item_path)
                    items_with_info.append({
                        'name': item,
                        'path': item_path,
                        'is_dir': is_dir,
                        'size': stat_info.st_size,
                        'mtime': stat_info.st_mtime,
                        'type': 'directory' if is_dir else 'file'
                    })
                except (OSError, PermissionError):
                    # Include items we can't stat but still list them
                    items_with_info.append({
                        'name': item,
                        'path': item_path,
                        'is_dir': False,
                        'size': 0,
                        'mtime': 0,
                        'type': 'unknown'
                    })
    except (OSError, PermissionError):
        return [] if not show_details else f"Permission denied: {path}"

    # Sort the items
    if sort_by == "name":
        items_with_info.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
    elif sort_by == "mtime":
        items_with_info.sort(key=lambda x: x['mtime'])
    elif sort_by == "size":
        items_with_info.sort(key=lambda x: (x['is_dir'], x['size']))
    elif sort_by == "type":
        items_with_info.sort(key=lambda x: (x['type'], x['name'].lower()))

    if reverse:
        items_with_info.reverse()

    # Return appropriate format
    if show_details:
        output_lines = [f"Directory: {path}"]
        output_lines.append(f"Total entries: {len(items_with_info)}")
        output_lines.append("")

        for item in items_with_info:
            prefix = "[DIR] " if item['is_dir'] else "[FILE]"
            size_str = f"{item['size']:,} bytes" if not item['is_dir'] else ""
            mtime_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(item['mtime'])) if item['mtime'] > 0 else "unknown"
            output_lines.append(f"{prefix}{item['name']:30} {size_str:15} {mtime_str}")

        return "\n".join(output_lines)
    else:
        return [item['name'] for item in items_with_info]