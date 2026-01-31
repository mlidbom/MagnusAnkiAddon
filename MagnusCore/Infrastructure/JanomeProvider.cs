namespace MagnusCore.Infrastructure;

using System.Diagnostics;
using Domain;
using Ports;
using Python.Runtime;

/// <summary>
/// Provides Japanese NLP via janome (Python library accessed through Python.NET)
/// Can work in two modes:
/// 1. Initialized from Python (when running in Anki) - reuses existing tokenizer
/// 2. Auto-initialized (standalone .NET) - creates own Python runtime and tokenizer
/// </summary>
public class JanomeProvider : IJapaneseNlpProvider
{
    private dynamic? _janomeTokenizer;
    private readonly object _initLock = new();
    private bool _initializedFromPython;

    /// <summary>
    /// Call this from Python to provide an existing janome tokenizer instance.
    /// This avoids creating a nested Python runtime when running in Anki.
    /// </summary>
    public void InitializeFromPython(dynamic janomeTokenizer)
    {
        lock (_initLock)
        {
            _janomeTokenizer = janomeTokenizer;
            _initializedFromPython = true;
            Console.WriteLine("[JanomeProvider] Initialized from Python with existing tokenizer");
        }
    }

    /// <summary>
    /// Automatically initializes Python and creates janome tokenizer if not already initialized.
    /// Called when running standalone in .NET.
    /// </summary>
    private void EnsureInitialized()
    {
        if (_janomeTokenizer != null) return;

        lock (_initLock)
        {
            if (_janomeTokenizer != null) return;

            Console.WriteLine("[JanomeProvider] Auto-initializing Python runtime...");

            // Initialize Python runtime if not already done
            if (!PythonEngine.IsInitialized)
            {
                PythonEngine.Initialize();
                PythonEngine.BeginAllowThreads();
            }

            using (Py.GIL())
            {
                try
                {
                    // Import janome
                    dynamic janome = Py.Import("janome.tokenizer");
                    _janomeTokenizer = janome.Tokenizer();
                    Console.WriteLine("[JanomeProvider] Created janome tokenizer in .NET");
                }
                catch (PythonException ex)
                {
                    throw new InvalidOperationException(
                        "Failed to initialize janome. Make sure janome is installed in the Python environment. " +
                        $"Error: {ex.Message}", ex);
                }
            }
        }
    }

    public List<Token> Tokenize(string text)
    {
        EnsureInitialized();

        var sw = Stopwatch.StartNew();
        List<Token> tokens;

        using (Py.GIL())
        {
            try
            {
                var pyTokens = _janomeTokenizer!.tokenize(text);
                tokens = new List<Token>();

                foreach (var t in pyTokens)
                {
                    // Convert Python token to C# DTO immediately
                    // Don't hold onto Python objects - they're GC'd differently
                    tokens.Add(new Token(
                        Surface: (string)t.surface,
                        BaseForm: (string)t.base_form,
                        PartOfSpeech: (string)t.part_of_speech,
                        Reading: (string)t.reading,
                        Phonetic: (string)t.phonetic,
                        InflectionType: (string)t.infl_type,
                        InflectionForm: (string)t.infl_form
                    ));
                }
            }
            catch (PythonException ex)
            {
                throw new InvalidOperationException($"Tokenization failed for text: {text}", ex);
            }
        }

        sw.Stop();
        Console.WriteLine($"[JanomeProvider] Tokenized {tokens.Count} tokens in {sw.ElapsedMilliseconds}ms");

        return tokens;
    }

    /// <summary>
    /// For debugging - shows whether tokenizer came from Python or was created in .NET
    /// </summary>
    public string GetInitializationMode()
    {
        if (_janomeTokenizer == null) return "Not initialized";
        return _initializedFromPython ? "Initialized from Python" : "Auto-initialized in .NET";
    }
}
