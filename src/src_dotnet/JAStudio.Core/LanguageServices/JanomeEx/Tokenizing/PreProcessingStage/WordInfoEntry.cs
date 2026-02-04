using System;
using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;

public abstract class WordInfoEntry
{
    public string Word { get; }
    public HashSet<string> PartsOfSpeech { get; }

    protected WordInfoEntry(string word, HashSet<string> partsOfSpeech)
    {
        Word = word;
        PartsOfSpeech = partsOfSpeech;
    }

    public bool IsIchidan => PartsOfSpeech.Contains("Ichidan verb");  // TODO: Use POS constants when ported
    public bool IsGodan => PartsOfSpeech.Contains("Godan verb");  // TODO: Use POS constants when ported
    public bool IsIntransitive => PartsOfSpeech.Contains("intransitive verb");  // TODO: Use POS constants when ported

    public abstract string Answer { get; }
}

public class VocabWordInfoEntry : WordInfoEntry
{
    private readonly VocabNote _vocab;

    public VocabWordInfoEntry(string word, VocabNote vocab)
        : base(word, vocab.PartsOfSpeech.Get())
    {
        _vocab = vocab;
    }

    public override string Answer => _vocab.GetAnswer();
}

public class DictWordInfoEntry : WordInfoEntry
{
    // TODO: Implement when DictLookupResult is ported
    private readonly object _dictResult;

    public DictWordInfoEntry(string word, object dictResult)
        : base(word, new HashSet<string>())  // TODO: Get parts of speech from dict result
    {
        _dictResult = dictResult;
    }

    public override string Answer => "TODO: Format answer from dict result";
}
