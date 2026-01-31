# Opening in Rider

## Step 1: Open the Solution

1. Launch **JetBrains Rider**
2. Click **Open**
3. Navigate to: `C:\Users\magnu\PycharmProjects\MagnusAnkiAddon`
4. Select **MagnusAnkiAddon.sln**
5. Click **Open**

Rider will load all three projects:
- MagnusCore (library)
- MagnusCore.Tests (tests)
- MagnusCore.Console (demo app)

## Step 2: Configure Python Interpreter

1. Go to **File → Settings** (Ctrl+Alt+S)
2. Navigate to **Languages & Frameworks → Python Interpreter**
3. Click **Add Interpreter → Existing environment**
4. Set interpreter to: `C:\Users\magnu\PycharmProjects\MagnusAnkiAddon\venv\Scripts\python.exe`
5. Click **OK**

## Step 3: Run the Tests

1. In Solution Explorer, right-click **MagnusCore.Tests**
2. Select **Run Unit Tests**
3. Watch the Test Explorer window for results

Or use the terminal in Rider:
```bash
dotnet test
```

## Step 4: Run the Console App

1. Click the run configuration dropdown (top right)
2. Select **MagnusCore.Console**
3. Click the green play button

Or use the terminal:
```bash
dotnet run --project MagnusCore.Console
```

## Step 5: Try the Python Example

In Rider's terminal:
```bash
python example_python_to_dotnet.py
```

## Useful Rider Features

### Cross-Language Navigation
- Ctrl+Click on `JanomeProvider` in Python → jumps to C# definition
- Ctrl+Click on C# method → shows all usages (including Python)

### Debugging Both Languages
1. Set breakpoint in `JanomeProvider.cs`
2. Run Python script in debug mode
3. Debugger stops at C# breakpoint when Python calls it

### Refactoring
- Rename a C# class → Rider updates Python imports
- Extract method → Works across both languages
- Find usages → Shows Python and C# references

### Test Runner
- Run individual tests by clicking the green arrow
- Debug tests with breakpoints
- See test output in real-time

## Project Structure in Rider

```
Solution 'MagnusAnkiAddon'
├─ MagnusCore
│  ├─ Dependencies
│  │  └─ pythonnet 3.0.5
│  ├─ Domain
│  │  └─ Token.cs
│  ├─ Infrastructure
│  │  └─ JanomeProvider.cs
│  ├─ Ports
│  │  └─ IJapaneseNlpProvider.cs
│  └─ Services
│     └─ TokenizerService.cs
│
├─ MagnusCore.Tests
│  └─ JanomeProviderTests.cs
│
├─ MagnusCore.Console
│  └─ Program.cs
│
└─ Python files (if you add the src folder)
   └─ example_python_to_dotnet.py
```

## Tips

1. **Enable solution-wide analysis**: Settings → Editor → Inspection Settings → Enable solution-wide analysis
2. **Code cleanup**: Ctrl+E, C (formats code, organizes usings)
3. **Navigate to anything**: Ctrl+T (type class/file name)
4. **Recent files**: Ctrl+E
5. **Build**: Ctrl+Shift+B
