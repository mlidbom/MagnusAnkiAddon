"""
Tests for Python to .NET interoperability.

These tests verify that Python can successfully load and call the C# JAStudio libraries.
"""
from __future__ import annotations

from typing import TYPE_CHECKING  # noqa: E402

from autoslot import Slots

#from typing import override
from jaslib.sysutils.timeutil import StopWatch
from JAStudio.Core.InteropExperiments import CustomTypeReceiver  # noqa: E402
from JAStudio.PythonInterop import JanomeTokenizer  # noqa: E402

if TYPE_CHECKING:
    from JAStudio.Core.Tokenization import Token


class PythonToken:
    def __init__(self, surface: str) -> None:
        self._surface:str = surface

    @property
    def surface(self) -> str: return self._surface

class PythonTokenSlots(Slots):
    def __init__(self, surface: str) -> None:
        self._surface:str = surface

    @property
    def surface(self) -> str: return self._surface

def test_can_tokenize_japanese_text_via_dotnet() -> None:
    provider = JanomeTokenizer()
    sentence = "すべての事実に一致する以上　それが正しい事は間違いない"
    tokens = provider.Tokenize(sentence)

    # Verify we got tokens back
    assert tokens is not None
    assert tokens.Count > 0

    # Check first token
    first_token = tokens[0]
    assert first_token.Surface == "すべて"

    print()

    tokenizing_iterations = 100
    with StopWatch.print_execution_time(f"Tokenize {tokenizing_iterations} sentences"):
        for _loop in range(tokenizing_iterations):  # pyright: ignore [reportUnusedVariable]
            tokens = provider.Tokenize(sentence)

    property_access_iterations = 100000
    left = property_access_iterations
    net_token:Token = tokens[0]
    with StopWatch.print_execution_time(f"Access {property_access_iterations} properties"):
        while left > 0:
            left -= 1
            something = net_token.Surface  # pyright: ignore  # noqa: F841

    left = property_access_iterations
    py_token = PythonToken(net_token.Surface)
    with StopWatch.print_execution_time(f"Loop with python object property access {property_access_iterations}"):
        while left > 0:
            left -= 1
            something = py_token.surface  # pyright: ignore  # noqa: F841

    left = property_access_iterations
    py_token_slots = PythonTokenSlots(net_token.Surface)
    with StopWatch.print_execution_time(f"Loop with python slots object property access {property_access_iterations}"):
        while left > 0:
            left -= 1
            something = py_token_slots.surface  # pyright: ignore  # noqa: F841

    left = property_access_iterations
    with StopWatch.print_execution_time(f"Loop with no property access {property_access_iterations}"):
        while left > 0:
            left -= 1

class CustomClass:
    # noinspection PyPep8Naming
    @property
    def AValue(self) -> str: return "Ao" #used from .NET that's why the name


def test_passing_custom_class_instance() -> None:
    receiver = CustomTypeReceiver()
    custom_subclass_instance = CustomClass()
    assert custom_subclass_instance.AValue == "Ao"
    assert receiver.ReceiveClass(custom_subclass_instance) == "Ao"
