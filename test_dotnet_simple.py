"""
Simple test to verify Python can load and call the C# DLL
"""

# Set the runtime to .NET Core BEFORE importing clr
from __future__ import annotations

from clr_loader import get_coreclr
from pythonnet import set_runtime

rt = get_coreclr()
set_runtime(rt)

# Now import clr with the correct runtime
import clr

dll_path = r"C:\Users\magnu\PycharmProjects\MagnusAnkiAddon\JAStudio.Core\bin\Debug\net10.0\JAStudio.Core.dll"

print(f"Loading: {dll_path}")
clr.AddReference(dll_path)

print("Imported! Accessing types...")

# The correct way to access .NET Core types with pythonnet 3.x
from System import Activator, Type

# Get the types by full name
janome_type = Type.GetType("JAStudio.Core.Infrastructure.JanomeProvider, JAStudio.Core")
service_type = Type.GetType("JAStudio.Core.Services.TokenizerService, JAStudio.Core")

print(f"✓ Found types: {janome_type.Name}, {service_type.Name}")

# Create Python janome
from janome.tokenizer import Tokenizer

python_tokenizer = Tokenizer()
print("✓ Created Python janome tokenizer")

# Create C# provider instance
provider = Activator.CreateInstance(janome_type)
print("✓ Created C# JanomeProvider")

# Pass Python instance to C#
provider.InitializeFromPython(python_tokenizer)
print("✓ Initialized provider with Python tokenizer")

# Use it to tokenize
sentence = "昨日、友達と映画を見ました。"
tokens = provider.Tokenize(sentence)

print(f"\n✓ Tokenized: {sentence}")
print(f"  Token count: {tokens.Count}")
for i in range(min(3, tokens.Count)):
    token = tokens[i]
    print(f"  {token.Surface} | {token.BaseForm}")

print("\n✓✓✓ Python → .NET integration WORKS! ✓✓✓")
