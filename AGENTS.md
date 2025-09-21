# Repository Guidelines

## Project Structure & Module Organization
- `main.py` is the entry point; keep reusable logic inside clear, importable functions so tests can import them.
- `pyproject.toml` defines metadata and runtime dependencies; add optional dev tools under `[project.optional-dependencies]`.
- Place unit tests in a `tests/` package that mirrors the module layout (e.g., `tests/test_main.py`). Store shared fixtures in `tests/conftest.py`.
- Keep README-level docs or larger design notes in Markdown files under a future `docs/` directory.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` creates an isolated environment; activate it before development.
- `pip install -e .[dev]` installs the package in editable mode along with declared dev dependencies.
- `python -m main` runs the CLI entry point locally to verify the greeting behavior.
- `pytest` executes the full automated test suite once it exists; combine with `pytest tests/test_main.py -k keyword` to target specific cases.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation, lowercase_with_underscores for modules and functions, and CapWords for classes.
- Type annotate public functions and keep functions under 50 lines; refactor larger routines into helpers.
- Prefer f-strings for formatting and include concise docstrings describing side effects or I/O.
- Before pushing, run `ruff check .` (add to dev dependencies) to catch lint issues and `ruff format` for consistent styling.

## Testing Guidelines
- Use `pytest` for unit tests; name files `test_*.py` and functions `test_<behavior>()`.
- Aim for ≥80% branch coverage once features stabilize; track with `pytest --cov=main --cov-report=term-missing`.
- Mock external services, but keep business logic tests deterministic; use parametrization for edge cases.

## Commit & Pull Request Guidelines
- Adopt Conventional Commit messages (e.g., `feat: add CLI greeting`) to make releases predictable.
- Commits should be focused and buildable; run lint and tests before committing.
- Pull requests need a summary of intent, testing evidence, and links to any tracking issues. Add screenshots or terminal output when behavior changes.

## Security & Configuration Tips
- Never commit secrets; use environment variables loaded via `.env` and add the filename to `.gitignore`.
- Review dependency updates for CVEs before merging and document required environment variables in `README.md`.
