from __future__ import annotations

from anki.models import NotetypeDict
from jaslib.sysutils import typed
from jastudio.ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules  # noqa  # pyright: ignore[reportUnusedImport]


def test_notetypedict() -> None:
    mydict:NotetypeDict = NotetypeDict()
    assert typed.checked_cast_generics(NotetypeDict, mydict) is mydict
    assert typed.checked_cast_dynamic(NotetypeDict, mydict) is mydict

def test_int() -> None:
    assert typed.int_(1) == 1
    assert typed.checked_cast(int, 1) == 1
    assert typed.checked_cast_generics(int, 1) == 1
    assert typed.checked_cast_dynamic(int, 1) == 1

def test_float() -> None:
    assert typed.float_(1.1) == 1.1
    assert typed.checked_cast(float, 1.1) == 1.1
    assert typed.checked_cast_generics(float, 1.1) == 1.1
    assert typed.checked_cast_dynamic(float, 1.1) == 1.1

def test_bool() -> None:
    assert typed.bool_(True) is True
    assert typed.bool_(False) is False
    assert typed.checked_cast(bool, True) is True
    assert typed.checked_cast_generics(bool, True) is True
    assert typed.checked_cast_dynamic(bool, True) is True

def test_str() -> None:
    value = "aoeu"
    assert typed.str_(value) is value
    assert typed.checked_cast(str, value) is value
    assert typed.checked_cast_generics(str, value) is value
    assert typed.checked_cast_dynamic(str, value) is value