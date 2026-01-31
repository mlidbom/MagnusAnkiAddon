"""
Example: Using MagnusCore from Python (simulating Anki addon usage)

This demonstrates how to:
1. Load the .NET assembly
2. Pass Python janome instance to C#
3. Call C# services from Python
4. Get results back as Python objects
"""

import sys
import os

# Ensure pythonnet is installed
try:
    import clr
except ImportError:
    print("Installing pythonnet...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pythonnet"])
    import clr

# Ensure janome is installed
try:
    from janome.tokenizer import Tokenizer
except ImportError:
    print("Installing janome...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "janome"])
    from janome.tokenizer import Tokenizer

# Point to the compiled C# DLL
# Adjust this path based on your build configuration
dll_path = os.path.join(
    os.path.dirname(__file__),
    "MagnusCore",
    "bin",
    "Debug",  # or "Release"
    "net8.0",
    "MagnusCore.dll"
)

if not os.path.exists(dll_path):
    print(f"ERROR: Could not find MagnusCore.dll at {dll_path}")
    print("\nYou need to build the C# project first:")
    print("  cd MagnusCore")
    print("  dotnet build")
    sys.exit(1)

print(f"Loading .NET assembly from: {dll_path}")
sys.path.append(os.path.dirname(dll_path))
clr.AddReference("MagnusCore")

# Import the C# types using pythonnet syntax
# The import path mirrors the C# namespace
import MagnusCore.Infrastructure as infra
import MagnusCore.Services as services

JanomeProvider = infra.JanomeProvider
TokenizerService = services.TokenizerService

print("Successfully loaded C# types!")

print("\n=== Python -> .NET Integration Example ===\n")

# Create Python janome tokenizer (as we would in Anki)
print("Creating Python janome tokenizer...")
python_tokenizer = Tokenizer()

# Create C# provider
print("Creating C# JanomeProvider...")
provider = JanomeProvider()

# Pass Python instance to C# (avoids nested Python runtime)
print("Passing Python tokenizer to C#...\n")
provider.InitializeFromPython(python_tokenizer)

# Create C# service
service = TokenizerService(provider)

# Example 1: Simple tokenization
print("=== Example 1: Calling C# from Python ===")
sentence = "昨日、友達と映画を見ました。"
result = service.Analyze(sentence)

# Access C# properties from Python
print(f"Sentence: {result.Text}")
print(f"Token count: {result.TokenCount}")
print(f"Unique base forms: {result.UniqueBaseForms}")

print("\nTokens (C# List accessed from Python):")
for token in result.Tokens:  # Iterating over C# List<Token>
    # Accessing C# record properties from Python
    print(f"  {token.Surface} | {token.BaseForm} | {token.PartOfSpeech}")

# Example 2: Extract verbs using C# logic
print("\n=== Example 2: C# Service Logic ===")
verbs = service.ExtractVerbs(sentence)
print(f"Found {len(verbs)} verb(s):")
for verb in verbs:
    print(f"  {verb.Surface} (base: {verb.BaseForm})")

# Show how it was initialized
print(f"\n=== Initialization Info ===")
print(f"Mode: {provider.GetInitializationMode()}")

print("\n✓ Successfully called C# from Python!")
print("\nThis is how the Anki addon will work:")
print("  1. Anki addon creates Python objects (janome, jamdict)")
print("  2. Passes them to C# via InitializeFromPython()")
print("  3. All heavy processing happens in C# with real threading")
print("  4. Results come back to Python for Anki integration")
