"""
Tests for Python to .NET interoperability.

These tests verify that Python can successfully load and call the C# JAStudio libraries.
"""
from __future__ import annotations

from time import sleep

from dotnet import dotnet_runtime_loader
from sysutils.timeutil import StopWatch

dotnet_runtime_loader.ensure_clr_loaded()

from JAStudio.PythonInterop import JanomeTokenizer  # noqa: E402


def test_can_tokenize_japanese_text_via_dotnet() -> None:
    provider = JanomeTokenizer()
    sentence = "昨日、友達と映画を見ました。"
    tokens = provider.Tokenize(sentence)

    # Verify we got tokens back
    assert tokens is not None
    assert tokens.Count > 0

    # Check first token
    first_token = tokens[0]
    assert first_token.Surface
    assert first_token.Surface == "昨日"

    print()

    iterations = 1000
    with StopWatch.print_execution_time(f"Tokenize {iterations} sentences"):
        for _loop in range(iterations):  # pyright: ignore [reportUnusedVariable]
            tokens = provider.Tokenize(sentence)

    print("""
    Done

""")
