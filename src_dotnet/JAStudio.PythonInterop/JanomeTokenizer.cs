using System;
using System.Collections.Generic;
using System.Threading;
using JAStudio.Core.Domain;
using JAStudio.Core.Tokenization;
using JetBrains.Annotations;
using Python.Runtime;

namespace JAStudio.PythonInterop;

public class JanomeTokenizer : ITokenizer
{
    private dynamic? _janomeTokenizer;
    private readonly Lock _initLock = new();

    [UsedImplicitly]
    public void InitializeFromPython(dynamic janomeTokenizer)
    {
        lock (_initLock)
        {
            _janomeTokenizer = janomeTokenizer;
            Console.WriteLine("[JanomeProvider] Initialized from Python with existing tokenizer");
        }
    }

    private void EnsureInitialized()
    {
        if (_janomeTokenizer != null) return;

        lock (_initLock)
        {
            if (_janomeTokenizer != null) return;

            Console.WriteLine("[JanomeProvider] Auto-initializing Python runtime...");
            
            if (!PythonEngine.IsInitialized)
            {
                PythonEngine.Initialize();
                PythonEngine.BeginAllowThreads();
            }

            using (Py.GIL())
            {
                try
                {
                    dynamic janome = Py.Import("janome.tokenizer");
                    _janomeTokenizer = janome.Tokenizer();
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

        List<Token> tokens;

        using (Py.GIL())
        {
            try
            {
                var pyTokens = _janomeTokenizer!.tokenize(text);
                tokens = new List<Token>();

                foreach (var t in pyTokens)
                {
                    // Convert to pure .NET objects immediately.
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

        return tokens;
    }
}