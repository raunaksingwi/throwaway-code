"""ast_grep tool - search for AST patterns in code files using ast-grep."""

import os
from pathlib import Path
from agents import function_tool
from ast_grep_py import SgRoot
from ._shared import security_error_handler, is_valid_path, logger


@function_tool(failure_error_function=security_error_handler)
def ast_grep(
    pattern: str,
    file_pattern: str = "**/*.py",
    language: str = "python",
    max_results: int = 50
) -> str:
    """
    Search for AST patterns in files within the workspace using ast-grep.

    This tool allows you to search for code patterns using AST (Abstract Syntax Tree)
    matching, which is more powerful than simple text search. It can find code structures
    like function definitions, class declarations, specific expressions, etc.

    Args:
        pattern: The AST pattern to search for (e.g., "def $FUNC($$$ARGS):", "class $CLASS:")
        file_pattern: File pattern to search in (default: "**/*.py")
        language: Programming language to parse (default: "python")
        max_results: Maximum number of results to return (default: 50)

    Returns:
        A formatted string containing all matches with file paths and line numbers

    Examples:
        - ast_grep("def $FUNC($$$ARGS):") - Find all function definitions
        - ast_grep("class $CLASS:") - Find all class definitions
        - ast_grep("print($A)") - Find all print statements
        - ast_grep("if $COND:", "**/*.js", "javascript") - Find if statements in JS files
    """
    if not pattern:
        raise ValueError("No pattern provided")

    workspace_root = os.getcwd()
    results = []
    files_searched = 0

    # Get all matching files
    for file_path in Path(workspace_root).glob(file_pattern):
        if file_path.is_file():
            # Validate the path is within workspace
            is_valid, _ = is_valid_path(str(file_path), workspace_root)
            if not is_valid:
                # Skip files outside workspace or ignored by .gitignore
                continue

            try:
                files_searched += 1

                # Read file content
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                if not content.strip():
                    continue

                # Parse with ast-grep
                try:
                    root = SgRoot(content, language)
                    root_node = root.root()

                    # Find all matches
                    matches = root_node.find_all(pattern=pattern)

                    for match in matches:
                        if len(results) >= max_results:
                            break

                        # Get match details
                        match_text = match.text()
                        match_range = match.range()
                        line_num = match_range.start.line + 1  # Convert to 1-based
                        col_num = match_range.start.column + 1  # Convert to 1-based

                        # Get relative path
                        rel_path = os.path.relpath(str(file_path), workspace_root)

                        # Format result
                        result = f"File: {rel_path}:{line_num}:{col_num}\n{match_text}\n"
                        results.append(result)

                except Exception as e:
                    # Skip files that can't be parsed (e.g., binary files, syntax errors)
                    logger.debug(f"Could not parse {file_path} with ast-grep: {e}")
                    continue

            except (PermissionError, UnicodeDecodeError):
                # Skip unreadable files
                continue

    if not results:
        return f"No matches found for pattern '{pattern}' in {files_searched} files searched."

    # Format final output
    output = f"Found {len(results)} matches for pattern '{pattern}' in {files_searched} files:\n\n"
    output += "=" * 80 + "\n\n"
    output += "\n".join(results)

    if len(results) >= max_results:
        output += f"\n\n... (showing first {max_results} results)"

    return output