# Magnus Core - .NET Migration Proof of Concept

This is a proof-of-concept demonstrating Python.NET integration for migrating the Magnus Anki addon to .NET.

## Project Structure

```
MagnusAnkiAddon/
├── MagnusCore/                     # C# class library
│   ├── Domain/                     # Pure C# data models
│   │   └── Token.cs               # janome token DTO
│   ├── Ports/                      # Interfaces (dependency inversion)
│   │   └── IJapaneseNlpProvider.cs
│   ├── Infrastructure/             # Python.NET integration
│   │   └── JanomeProvider.cs      # Calls janome via Python.NET
│   └── Services/                   # Business logic (pure C#)
│       └── TokenizerService.cs
│
├── MagnusCore.Tests/               # xUnit tests
│   └── JanomeProviderTests.cs     # Tests running .NET → Python
│
├── MagnusCore.Console/             # Standalone console app
│   └── Program.cs                 # Demo of .NET calling janome
│
└── example_python_to_dotnet.py    # Python calling .NET (Anki scenario)
```

## How It Works

### Scenario 1: Standalone .NET Application
```
.NET Process
└─ Embeds Python Runtime via Python.NET
   └─ Loads janome
      └─ C# calls Python
```

**Run**: `dotnet run --project MagnusCore.Console`

### Scenario 2: Anki Addon (Python Host)
```
Python Process (Anki)
├─ Creates janome tokenizer
└─ Loads .NET assembly via pythonnet
   └─ Passes Python tokenizer to C#
      └─ C# uses same Python instance
```

**Run**: `python example_python_to_dotnet.py`

## Quick Start

### 1. Build the C# Projects

```powershell
# Build everything
dotnet build

# Or build in Release mode
dotnet build -c Release
```

### 2. Run the Tests

```powershell
# Run all tests
dotnet test

# Run with verbose output
dotnet test --logger "console;verbosity=detailed"
```

**Expected output:**
```
Initializing Python runtime for tests...
[JanomeProvider] Auto-initializing Python runtime...
[JanomeProvider] Created janome tokenizer in .NET
[JanomeProvider] Tokenized 1 tokens in 45ms
✓ Should_Tokenize_Simple_Japanese_Text
...
```

### 3. Run Standalone Console App

```powershell
dotnet run --project MagnusCore.Console
```

**Expected output:**
```
=== Magnus Core - Standalone Example ===

Using Python from: C:\Users\magnu\PycharmProjects\MagnusAnkiAddon\venv
Python runtime initialized successfully!

=== Example 1: Simple Word ===
Surface: 食べる
Base Form: 食べる
Reading: タベル
...
```

### 4. Test Python → .NET Integration

```powershell
# Make sure pythonnet is installed
pip install pythonnet

# Run the example
python example_python_to_dotnet.py
```

**Expected output:**
```
Loading .NET assembly from: ...\MagnusCore.dll
Creating Python janome tokenizer...
Creating C# JanomeProvider...
Passing Python tokenizer to C#...

=== Example 1: Calling C# from Python ===
Sentence: 昨日、友達と映画を見ました。
Token count: 8
...
```

## Key Concepts Demonstrated

### 1. Dual Initialization Mode

The `JanomeProvider` can work two ways:

**From .NET** (auto-initialize):
```csharp
var provider = new JanomeProvider();
// Automatically creates Python runtime and janome instance
```

**From Python** (reuse existing):
```python
tokenizer = Tokenizer()  # Python creates
provider.InitializeFromPython(tokenizer)  # C# uses it
```

### 2. Clean Boundaries

- **Domain**: Pure C# records (no Python)
- **Ports**: Interfaces (swappable implementations)
- **Infrastructure**: Python.NET integration (isolated)
- **Services**: Pure business logic (testable)

### 3. GIL Management

```csharp
using (Py.GIL())  // Acquire Global Interpreter Lock
{
    // Python calls happen here
    var result = _tokenizer.tokenize(text);
}
// GIL released - C# code runs freely
```

### 4. Type Conversion

Python objects → C# DTOs immediately:
```csharp
foreach (var t in pyTokens)  // Python iterator
{
    tokens.Add(new Token(     // C# record
        Surface: (string)t.surface,  // Python → C#
        ...
    ));
}
// Now pure C# - no Python objects held
```

## Next Steps

This POC proves that:
1. ✅ C# can call janome via Python.NET
2. ✅ Python can call C# services seamlessly
3. ✅ Both modes work (Anki and standalone)
4. ✅ Tests run in .NET with Python integration
5. ✅ Performance is measurable (see console output)

**To migrate your actual code:**
1. Extract pure Python logic to `magnus_core` package (no Anki deps)
2. Port `magnus_core` to C# using this structure
3. Keep Anki integration in Python (thin adapter)
4. Incrementally move more logic to C#

## Troubleshooting

### "Could not load pythonnet"
```powershell
pip install pythonnet
```

### "Could not find python312.dll"
Update the path in `Program.cs` to match your venv location.

### "Could not import janome"
```powershell
pip install janome
```

### Tests fail with Python errors
Make sure janome is installed in your Python environment:
```powershell
pip show janome
```

## Performance Notes

The console app and tests show timing information. Typical results:
- First tokenization: ~100ms (Python startup)
- Subsequent: ~5-50ms depending on text length
- GIL acquisition: <1ms

The real performance gains come from:
- Caching tokenization results (in .NET memory)
- Parallel processing of multiple sentences (C# side)
- Efficient collection management (ConcurrentDictionary, etc.)

## Resources

- Python.NET Docs: https://pythonnet.github.io/
- Janome: https://mocobeta.github.io/janome/en/
- xUnit: https://xunit.net/
