using System;
using System.Collections.Generic;
using JAStudio.Core.Tokenization;
using Python.Runtime;

namespace JAStudio.PythonInterop.Janome;

public class JanomeTokenizer : ITokenizer
{
    private readonly dynamic? _janomeTokenizer;

    public JanomeTokenizer()
    {
        using (Py.GIL())
        {
            dynamic janome = Py.Import("janome.tokenizer");
            _janomeTokenizer = janome.Tokenizer();
        }
    }


    public List<Token> Tokenize(string text)
    {
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