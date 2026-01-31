using JAStudio.Core.Services;
using JAStudio.PythonInterop;

Console.WriteLine("=== JAStudio Core - Standalone Example ===");

try
{
    // Initialize Python environment
    PythonEnvironment.Initialize();
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
