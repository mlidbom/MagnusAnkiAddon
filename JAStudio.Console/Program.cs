using JAStudio.Core.Infrastructure;
using JAStudio.Core.Services;
using Python.Runtime;

Console.WriteLine("=== JAStudio Core - Standalone Example ===");

try
{
    // Auto-detect venv relative to executable
    var exeDir = AppDomain.CurrentDomain.BaseDirectory;
    var projectRoot = Path.GetFullPath(Path.Combine(exeDir, "..", "..", "..", ".."));
    var venvPath = Path.Combine(projectRoot, "venv");
    
    // Read pyvenv.cfg to find base Python
    var pyvenvCfg = Path.Combine(venvPath, "pyvenv.cfg");
    string? basePython = null;
    
    if (File.Exists(pyvenvCfg))
    {
        foreach (var line in File.ReadAllLines(pyvenvCfg))
        {
            if (line.StartsWith("home = "))
            {
                basePython = line.Substring(7).Trim();
                break;
            }
        }
    }
    
    if (basePython == null)
    {
        Console.WriteLine($"ERROR: Could not find base Python from {pyvenvCfg}");
        Console.WriteLine("Make sure the venv exists and has pyvenv.cfg");
        return 1;
    }
    
    // Find Python DLL (try venv first, then base)
    // Prefer version-specific DLLs (python313.dll) over generic (python3.dll)
    var pythonDll = Directory.GetFiles(Path.Combine(venvPath, "Scripts"), "python3??.dll")
        .OrderByDescending(f => f)
        .FirstOrDefault()
        ?? Directory.GetFiles(basePython, "python3??.dll")
        .OrderByDescending(f => f)
        .FirstOrDefault();
    
    if (pythonDll == null)
    {
        Console.WriteLine($"ERROR: Could not find Python DLL in {venvPath} or {basePython}");
        return 1;
    }
    
    Console.WriteLine($"Using venv: {venvPath}");
    Console.WriteLine($"Base Python: {basePython}");
    Console.WriteLine($"Python DLL: {pythonDll}");
    
    Runtime.PythonDLL = pythonDll;
    PythonEngine.PythonHome = basePython;
    PythonEngine.PythonPath = string.Join(
        Path.PathSeparator.ToString(),
        Path.Combine(basePython, "Lib"),
        Path.Combine(venvPath, "Lib", "site-packages"),
        Path.Combine(basePython, "DLLs")
    );

    // Initialize Python runtime
    PythonEngine.Initialize();
    PythonEngine.BeginAllowThreads();

    Console.WriteLine("Python runtime initialized successfully!\n");

    // Create provider (will auto-initialize janome)
    var provider = new JanomeProvider();
    var service = new TokenizerService(provider);

    // Example 1: Simple tokenization
    Console.WriteLine("=== Example 1: Simple Word ===");
    var tokens1 = provider.Tokenize("食べる");
    foreach (var token in tokens1)
    {
        Console.WriteLine($"Surface: {token.Surface}");
        Console.WriteLine($"Base Form: {token.BaseForm}");
        Console.WriteLine($"Reading: {token.Reading}");
        Console.WriteLine($"Part of Speech: {token.PartOfSpeech}\n");
    }

    // Example 2: Full sentence
    Console.WriteLine("=== Example 2: Sentence Analysis ===");
    var sentence = "昨日、友達と映画を見ました。";
    var result = service.Analyze(sentence);

    Console.WriteLine($"Sentence: {result.Text}");
    Console.WriteLine($"Token count: {result.TokenCount}");
    Console.WriteLine($"Unique base forms: {result.UniqueBaseForms}\n");

    Console.WriteLine("Tokens:");
    foreach (var token in result.Tokens)
    {
        Console.WriteLine($"  {token.Surface,-8} | {token.BaseForm,-8} | {token.PartOfSpeech}");
    }

    // Example 3: Extract verbs
    Console.WriteLine("\n=== Example 3: Extract Verbs ===");
    var verbs = service.ExtractVerbs(sentence);
    foreach (var verb in verbs)
    {
        Console.WriteLine($"  {verb.Surface} ({verb.BaseForm})");
    }

    // Show initialization info
    Console.WriteLine($"\n=== Initialization Info ===");
    Console.WriteLine($"Mode: {provider.GetInitializationMode()}");

    Console.WriteLine("\n✓ All examples completed successfully!");
}
catch (Exception ex)
{
    Console.WriteLine($"\n✗ Error: {ex.Message}");
    Console.WriteLine($"\nStack trace:\n{ex.StackTrace}");

    if (ex.InnerException != null)
    {
        Console.WriteLine($"\nInner exception: {ex.InnerException.Message}");
    }

    return 1;
}
finally
{
    // Note: PythonEngine.Shutdown() has issues with .NET 10 (BinaryFormatter)
    // Not calling it is fine - process exit will clean up Python
    // if (PythonEngine.IsInitialized)
    // {
    //     PythonEngine.Shutdown();
    // }
}

return 0;
