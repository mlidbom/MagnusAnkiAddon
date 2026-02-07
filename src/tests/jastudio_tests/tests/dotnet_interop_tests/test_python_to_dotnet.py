"""
Tests for Python to .NET interoperability.

These tests verify that Python can successfully load and call the C# JAStudio libraries.
"""
from __future__ import annotations  # noqa: I001


from jastudio.dotnet import load_dotnet_runtime

print(load_dotnet_runtime.config_file)

#from typing import override
from JAStudio.Core.InteropExperiments import CustomTypeReceiver  # noqa: E402


class CustomClass:
    @property
    def a_value(self) -> str: return "Ao" #used from .NET that's why the name


def test_passing_custom_class_instance() -> None:
    receiver = CustomTypeReceiver()
    custom_subclass_instance = CustomClass()
    assert custom_subclass_instance.a_value == "Ao"
    assert receiver.ReceiveClass(custom_subclass_instance) == "Ao"
