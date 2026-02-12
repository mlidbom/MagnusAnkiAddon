# Python Code Guidelines

**Scope:** This applies to all Python code in:
- `src/jastudio_src/` - Anki addon integration
- `src/jaspythonutils_src/` - Python utilities
- `src/jaslib_src/` - Python libraries
- `src/tests/` - Python tests
- `src/MagnusAddon/`, `src/MagnusAddonTests/` - Legacy (mostly empty, ignore)

## Critical Rules

### Minimize Python Code
This project is actively porting from Python to C#. **Do NOT expand Python functionality:**
- ❌ Don't add new Python business logic
- ❌ Don't add new Python UI code
- ✅ Only add Python code when interfacing with Anki APIs
- ✅ Prefer moving logic to C# (`JAStudio.Core` or `JAStudio.UI`)

### Type Safety is Mandatory
- ✅ **All functions must have complete type hints** (parameters and return types)
- ✅ Use `from typing import` or `from collections.abc import` for generic types
- ❌ **Never suppress type errors** without explicit permission
- ✅ Fix code to satisfy basedpyright instead of suppressing

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
- Line length: not strictly enforced (ruff is configured with a very high limit)
- Use f-strings for string formatting
- Prefer list/dict comprehensions over map/filter where readable
- **ruff** is the primary linter and formatter — configured in `pyproject.toml`
