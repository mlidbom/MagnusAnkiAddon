using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.PythonInterop.Tokenization;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.PythonInterop.Janome;

public class JanomeTokenizer : ITokenizer
{
    private readonly dynamic _janomeTokenizer;

    public JanomeTokenizer()
    {
        using (PythonEnvironment.LockGil())
        {
            dynamic janome = Py.Import("janome.tokenizer");
            _janomeTokenizer = janome.Tokenizer();
        }
    }


    public List<Token> Tokenize(string text) => PythonEnvironment.Use(() =>
        ((IEnumerable<dynamic>)Dyn.Enumerate(_janomeTokenizer.tokenize(text)))
        .Select(t => new Token(
            Surface: (string)t.surface,
            BaseForm: (string)t.base_form,
            PartOfSpeech: (string)t.part_of_speech,
            Reading: (string)t.reading,
            Phonetic: (string)t.phonetic,
            InflectionType: (string)t.infl_type,
            InflectionForm: (string)t.infl_form
        )).ToList());
}