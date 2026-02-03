using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Sentences;

public class WordExclusion
{
    public string Word { get; set; }
    public int Index { get; set; }

    private WordExclusion(string word, int index)
    {
        Word = word;
        Index = index;
    }

    public static WordExclusion Global(string word)
    {
        return new WordExclusion(word, -1);
    }

    public static WordExclusion AtIndex(string word, int index)
    {
        return new WordExclusion(word, index);
    }

    public bool ExcludesFormAtIndex(string word, int index)
    {
        if (Word != word)
            return false;

        if (Index == -1)
            return true;

        return Index == index;
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
        return new WordExclusion(reader.GetString("word"), reader.GetInt("index"));
    }

    public override string ToString()
    {
        return Index == -1 ? $"Global({Word})" : $"{Word}@{Index}";
    }
}

public class JsonReader
{
    private readonly Dictionary<string, object> _data;

    public JsonReader(Dictionary<string, object> data)
    {
        _data = data;
    }

    public string GetString(string key)
    {
        return _data.TryGetValue(key, out var value) ? value?.ToString() ?? "" : "";
    }

    public int GetInt(string key)
    {
        if (_data.TryGetValue(key, out var value))
        {
            if (value is int intValue) return intValue;
            if (int.TryParse(value?.ToString(), out var parsed)) return parsed;
        }
        return 0;
    }

    public List<string> GetStringList(string key, List<string> defaultValue)
    {
        if (_data.TryGetValue(key, out var value) && value is List<object> list)
        {
            return list.Select(o => o.ToString() ?? "").ToList();
        }
        return defaultValue;
    }

    public List<T> GetObjectList<T>(string key, Func<JsonReader, T> factory, List<T> defaultValue)
    {
        if (_data.TryGetValue(key, out var value) && value is List<object> list)
        {
            return list.Select(o => factory(new JsonReader(o as Dictionary<string, object> ?? new Dictionary<string, object>()))).ToList();
        }
        return defaultValue;
    }
}

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

    public static WordExclusionSet Empty(Action saveCallback)
    {
        return new WordExclusionSet(saveCallback, new List<WordExclusion>());
    }

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
