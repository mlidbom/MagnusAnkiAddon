"""
Tests for Python to .NET interoperability.

These tests verify that Python can successfully load and call the C# JAStudio libraries.
"""
from __future__ import annotations

import pytest


@pytest.fixture(scope="module", autouse=True)
def ensure_dotnet_loaded() -> None:
    """Ensure .NET runtime and assemblies are loaded before any tests run."""
    from dotnet import dotnet_runtime_loader
    dotnet_runtime_loader.ensure_clr_loaded()

def test_can_access_dotnet_types() -> None:
    """Test that we can access .NET types from the assembly."""
    from JAStudio.Core.Services import TokenizerService
    from JAStudio.PythonInterop import JanomeProvider

    assert JanomeProvider is not None
    assert TokenizerService is not None

def test_can_create_dotnet_instances() -> None:
    """Test that we can create instances of .NET types."""
    from JAStudio.PythonInterop import JanomeProvider

    provider = JanomeProvider()
    assert provider is not None

def test_can_pass_python_object_to_dotnet() -> None:
    """Test that we can pass Python objects to .NET and call methods."""
    from janome.tokenizer import Tokenizer
    from JAStudio.PythonInterop import JanomeProvider

    # Create Python janome tokenizer
    python_tokenizer = Tokenizer()

    # Create C# provider
    provider = JanomeProvider()

    # Pass Python instance to C#
    provider.InitializeFromPython(python_tokenizer)

    # This should not raise an exception
    assert provider is not None

def test_can_tokenize_japanese_text_via_dotnet() -> None:
    """Test that we can tokenize Japanese text through the .NET provider."""
    from janome.tokenizer import Tokenizer
    from JAStudio.PythonInterop import JanomeProvider

    # Create and initialize provider
    python_tokenizer = Tokenizer()
    provider = JanomeProvider()
    provider.InitializeFromPython(python_tokenizer)

    # Tokenize Japanese sentence
    sentence = "昨日、友達と映画を見ました。"
    tokens = provider.Tokenize(sentence)

    # Verify we got tokens back
    assert tokens is not None
    assert tokens.Count > 0

    tokens.Count

    # Check first token
    first_token = tokens[0]
    assert hasattr(first_token, 'Surface')
    assert hasattr(first_token, 'BaseForm')
    assert first_token.Surface == "昨日"

def test_can_use_tokenizer_service() -> None:
    """Test that we can use the TokenizerService with a Python provider."""
    from janome.tokenizer import Tokenizer
    from JAStudio.Core.Services import TokenizerService
    from JAStudio.PythonInterop import JanomeProvider

    # Create provider
    python_tokenizer = Tokenizer()
    provider = JanomeProvider()
    provider.InitializeFromPython(python_tokenizer)

    # Create service
    service = TokenizerService(provider)

    # Use the service
    sentence = "私は学生です。"
    result = service.Analyze(sentence)

    assert result is not None
    assert result.Tokens is not None
    assert result.TokenCount > 0
    assert result.Text == sentence
