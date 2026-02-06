using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;

namespace JAStudio.Core.Note.Sentences;

public class WordExclusionSet
{
    private readonly Action _saveCallback;
    private readonly HashSet<WordExclusion> _exclusions;
    private HashSet<string> _excludedWords;

    public WordExclusionSet(Action saveCallback, List<WordExclusion> exclusions)
    {
        _saveCallback = saveCallback;
        _exclusions = new HashSet<WordExclusion>(exclusions ?? new List<WordExclusion>());
        _excludedWords = ExtractWords();
    }

    public static WordExclusionSet Empty()
    {
        return new WordExclusionSet(() => { }, new List<WordExclusion>());
    }

    public static WordExclusionSet Empty(Action saveCallback) => new(saveCallback, new List<WordExclusion>());

    public bool IsEmpty() => !_exclusions.Any();

    public IEnumerable<WordExclusion> Get() => _exclusions;

    private HashSet<string> ExtractWords()
    {
        return _exclusions.Select(e => e.Word).ToHashSet();
    }

    public HashSet<string> Words() => _excludedWords;

    public void Reset()
    {
        _exclusions.Clear();
        _excludedWords.Clear();
        _saveCallback();
    }

    public void AddGlobal(string vocab)
    {
        Add(WordExclusion.Global(vocab));
    }

    public void Add(WordExclusion exclusion)
    {
        _exclusions.Add(exclusion);
        _excludedWords = ExtractWords();
        _saveCallback();
    }

    public void Remove(WordExclusion exclusion)
    {
        _exclusions.Remove(exclusion);
        _excludedWords = ExtractWords();
        _saveCallback();
    }

    public void RemoveString(string toRemove)
    {
        var toRemoveList = _exclusions.Where(ex => ex.Word == toRemove).ToList();
        foreach (var exclusion in toRemoveList)
        {
            _exclusions.Remove(exclusion);
        }
        _excludedWords = ExtractWords();
        _saveCallback();
    }

    public bool ExcludesAtIndex(string word, int index)
    {
        return _exclusions.Any(exclusion => exclusion.ExcludesFormAtIndex(word, index));
    }

    public override string ToString()
    {
        return string.Join(", ", _exclusions.Select(e => e.ToString()));
    }
}
