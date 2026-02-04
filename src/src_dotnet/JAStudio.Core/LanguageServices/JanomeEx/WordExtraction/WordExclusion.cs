using System;
using System.Collections.Generic;
using JAStudio.Core.SysUtils.Json;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;

public sealed class WordExclusion
{
    private const string Secret = "aoesunth9cgrcgf";
    private const int NoIndex = -1;

    public string Word { get; }
    public int Index { get; }
    private readonly string _matchPart;

    private WordExclusion(string word, int index, string secret)
    {
        if (secret != Secret)
        {
            throw new InvalidOperationException("please use the factory methods instead of this private constructor");
        }
        
        Word = word;
        Index = index;
        _matchPart = word.Split('｜')[0]; // VocabNoteQuestion.DISAMBIGUATION_MARKER
    }

    public bool ExcludesFormAtIndex(string form, int index)
    {
        return form == Word && (Index == NoIndex || Index == index);
    }

    public static WordExclusion Global(string exclusion)
    {
        return new WordExclusion(exclusion.Trim(), NoIndex, Secret);
    }

    public static WordExclusion AtIndex(string exclusion, int index)
    {
        return new WordExclusion(exclusion.Trim(), index, Secret);
    }

    public override bool Equals(object? obj)
    {
        if (obj is WordExclusion other)
        {
            return Word == other.Word && Index == other.Index;
        }
        return false;
    }

    public override int GetHashCode()
    {
        return HashCode.Combine(Word, Index);
    }

    public override string ToString()
    {
        return $"WordExclusion('{Word}', {Index})";
    }

    public bool ExcludesAllWordsExcludedBy(WordExclusion other)
    {
        return Word == other.Word && (Index == NoIndex || Index == other.Index);
    }

    public Dictionary<string, object> ToDict()
    {
        return new Dictionary<string, object>
        {
            { "word", Word },
            { "index", Index }
        };
    }

    public static WordExclusion FromReader(JsonReader reader)
    {
        return new WordExclusion(
            reader.GetString("word"),
            reader.GetInt("index"),
            Secret
        );
    }
}
