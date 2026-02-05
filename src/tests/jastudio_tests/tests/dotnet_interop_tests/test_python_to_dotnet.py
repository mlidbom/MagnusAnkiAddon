"""
Tests for Python to .NET interoperability.

These tests verify that Python can successfully load and call the C# JAStudio libraries.
"""
from __future__ import annotations

#from typing import override
from JAStudio.Core.InteropExperiments import CustomTypeReceiver  # noqa: E402

# noinspection Annotator
from jastudio.dotnet import load_dotnet_runtime  # pyright: ignore [reportUnusedImport]  # noqa: F401


class CustomClass:
    # noinspection PyPep8Naming
    @property
    def AValue(self) -> str: return "Ao" #used from .NET that's why the name


def test_passing_custom_class_instance() -> None:
    receiver = CustomTypeReceiver()
    custom_subclass_instance = CustomClass()
    assert custom_subclass_instance.AValue == "Ao"
    assert receiver.ReceiveClass(custom_subclass_instance) == "Ao"
