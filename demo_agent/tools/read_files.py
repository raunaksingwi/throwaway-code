"""read_files tool - read the contents of one or more files."""

from typing import Optional
from agents import function_tool
from ._shared import security_error_handler, is_valid_path


@function_tool(failure_error_function=security_error_handler)
def read_files(
    files: list[str],
    include_line_numbers: bool = False,
    max_lines_per_file: Optional[int] = None,
    encoding: str = "utf-8"
) -> str:
    """
    Read the contents of one or more files within the workspace, respecting .gitignore patterns.
    Args:
        files: A list of files to read.
        include_line_numbers: Add line numbers to the output (default: False)
        max_lines_per_file: Maximum lines to read per file (default: None for unlimited)
        encoding: Text encoding to use (default: "utf-8")
    Returns:
        A string containing the contents of all files, with file headers for multi-file reads.
    Raises:
        ValueError: If no files provided or invalid parameters
        ValueError: If any file is outside the workspace or should be ignored
    """
    if not files:
        raise ValueError("No files provided")

    if max_lines_per_file is not None and max_lines_per_file < 1:
        raise ValueError("max_lines_per_file must be >= 1")

    result_parts = []
    
    for file in files:
        is_valid, validated_path = is_valid_path(file)
        if not is_valid:
            raise ValueError(f"Invalid or inaccessible file path: {file}")

        try:
            with open(validated_path, "r", encoding=encoding, errors="ignore") as f:
                if max_lines_per_file is not None:
                    # Read line by line with limit
                    lines = []
                    for i, line in enumerate(f, 1):
                        if i > max_lines_per_file:
                            lines.append(f"... (truncated after {max_lines_per_file} lines)")
                            break
                        lines.append(line.rstrip('\n\r'))

                    if include_line_numbers:
                        numbered_lines = []
                        for i, line in enumerate(lines, 1):
                            if line.startswith("... (truncated"):
                                numbered_lines.append(line)
                            else:
                                numbered_lines.append(f"{i:4d}: {line}")
                        content = "\n".join(numbered_lines)
                    else:
                        content = "\n".join(lines)
                else:
                    # Read entire file
                    content = f.read()
                    if include_line_numbers:
                        lines = content.split('\n')
                        numbered_lines = [f"{i:4d}: {line}" for i, line in enumerate(lines, 1)]
                        content = "\n".join(numbered_lines)

                # Add file header for multi-file reads
                if len(files) > 1:
                    result_parts.append(f"=== File: {file} ===\n{content}\n")
                else:
                    result_parts.append(content)

        except UnicodeDecodeError as e:
            raise ValueError(f"Cannot decode file {file} with encoding {encoding}: {e}")
        except OSError as e:
            raise ValueError(f"Cannot read file {file}: {e}")
    
    return "\n".join(result_parts)