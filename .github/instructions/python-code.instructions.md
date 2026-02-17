---
applyTo: "**/*.py"
---

# Python Code Guidelines

**Scope:** This applies to all Python

## Critical Rules

### Minimize Python Code
This project is actively porting from Python to C#. **Do NOT expand Python functionality:**
- ✅ Prefer moving logic to C#

### Type Safety is Mandatory
- ✅ **All functions must have complete type hints** (parameters and return types)
- ✅ Use `from typing import` or `from collections.abc import` for generic types
- ❌ **Never suppress type errors** without explicit permission
- ✅ Fix code to satisfy basedpyright instead of suppressing

### `from __future__ import annotations` is Required
Every Python file must start with `from __future__ import annotations`. This is enforced by ruff (`isort.required-imports` in `pyproject.toml`). Missing it causes lint failures and can cause other type-related warnings to not appear.

**Example:**
```python
# ✅ GOOD - Complete type hints
from collections.abc import Sequence

def process_items(items: Sequence[str], count: int) -> list[str]:
    return list(items[:count])

# ❌ BAD - Missing type hints
def process_items(items, count):
    return list(items[:count])
```

### Integration with C#
When Python needs to call C# code:
- Import from `typings/` (auto-generated Python stubs for C# APIs)
- Use pythonnet's `.NET` types correctly
- Handle exceptions from C# appropriately (they propagate as Python exceptions)
- **Stubs can be stale**: If a C# API was just changed, run `.\full-build.ps1` (which regenerates stubs) before relying on `typings/` for the new API surface

**Example:**
```python
from JAStudio.Core.Note import KanjiNote, SentenceNote, VocabNote

# Use C# types from Python — stubs in typings/ provide type info
note = KanjiNote.Create(data)
```

### Testing
- Python test directories: `src/tests/jaspythonutils_tests/`, `src/tests/jaslib_tests/`, `src/tests/jastudio_tests/` — choose based on what code is under test
- Follow existing pytest patterns
- Use type hints in test code too
- Run: `pytest`

## Code Style
- Follow PEP 8
- Use 4-space indentation
- Line length: effectively unlimited (`line-length = 320` in `pyproject.toml`)
- Use f-strings for string formatting
- Prefer list/dict comprehensions over map/filter where readable
- **ruff** is the sole linter configured in `pyproject.toml`
  - `ruff check --fix` — lint + autofix

## Comments
- Don't add comments unless they match existing style or explain complex logic
- Prefer self-documenting code over comments
- Update comments when changing code
