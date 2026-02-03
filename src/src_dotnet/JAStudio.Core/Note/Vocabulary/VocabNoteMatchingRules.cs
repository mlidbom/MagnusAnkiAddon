using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMatchingRulesData
{
    public HashSet<string> PrefixIsNot { get; set; } = new();
    public HashSet<string> SuffixIsNot { get; set; } = new();
    public HashSet<string> SurfaceIsNot { get; set; } = new();
    public HashSet<string> YieldToSurface { get; set; } = new();
    public HashSet<string> RequiredPrefix { get; set; } = new();

    public VocabNoteMatchingRulesData()
    {
    }

    public VocabNoteMatchingRulesData(HashSet<string> surfaceIsNot, HashSet<string> prefixIsNot, 
        HashSet<string> suffixIsNot, HashSet<string> requiredPrefix, HashSet<string> yieldToSurface)
    {
        SurfaceIsNot = surfaceIsNot;
        PrefixIsNot = prefixIsNot;
        SuffixIsNot = suffixIsNot;
        RequiredPrefix = requiredPrefix;
        YieldToSurface = yieldToSurface;
    }
}

public class VocabNoteMatchingRulesSerializer
{
    // Stub serializer - will implement with JSON later
    public VocabNoteMatchingRulesData Deserialize(string serialized)
    {
        if (string.IsNullOrEmpty(serialized))
            return new VocabNoteMatchingRulesData();
        
        // Stub: Just return empty data for now
        return new VocabNoteMatchingRulesData();
    }

    public string Serialize(VocabNoteMatchingRulesData instance)
    {
        // Stub: Return empty string for now
        if (instance.SurfaceIsNot.Count == 0 && instance.PrefixIsNot.Count == 0 &&
            instance.SuffixIsNot.Count == 0 && instance.RequiredPrefix.Count == 0 &&
            instance.YieldToSurface.Count == 0)
        {
            return string.Empty;
        }
        
        // Stub: Return non-empty marker
        return "{}";
    }
}

public class VocabNoteMatchingRules
{
    private readonly VocabNote _vocab;
    private readonly VocabNoteMatchingRulesData _data;

    public HashSet<string> SurfaceIsNot { get; }
    public HashSet<string> YieldToSurface { get; }
    public HashSet<string> PrefixIsNot { get; }
    public HashSet<string> SuffixIsNot { get; }
    public HashSet<string> RequiredPrefix { get; }

    public VocabNoteMatchingRules(VocabNote vocab)
    {
        _vocab = vocab;
        // Stub: Create empty data for now
        _data = new VocabNoteMatchingRulesData();
        
        SurfaceIsNot = _data.SurfaceIsNot;
        YieldToSurface = _data.YieldToSurface;
        PrefixIsNot = _data.PrefixIsNot;
        SuffixIsNot = _data.SuffixIsNot;
        RequiredPrefix = _data.RequiredPrefix;
    }

    public int MatchWeight
    {
        get
        {
            int weight = 0;
            if (RequiredPrefix.Any())
                weight += 10;
            
            if (SurfaceIsNot.Any()) weight += 2;
            if (YieldToSurface.Any()) weight += 2;
            if (PrefixIsNot.Any()) weight += 2;
            if (SuffixIsNot.Any()) weight += 2;
            if (RequiredPrefix.Any()) weight += 2;
            
            return weight;
        }
    }

    public void OverwriteWith(VocabNoteMatchingRules other)
    {
        SurfaceIsNot.Clear();
        foreach (var item in other.SurfaceIsNot) SurfaceIsNot.Add(item);
        
        YieldToSurface.Clear();
        foreach (var item in other.YieldToSurface) YieldToSurface.Add(item);
        
        PrefixIsNot.Clear();
        foreach (var item in other.PrefixIsNot) PrefixIsNot.Add(item);
        
        SuffixIsNot.Clear();
        foreach (var item in other.SuffixIsNot) SuffixIsNot.Add(item);
        
        RequiredPrefix.Clear();
        foreach (var item in other.RequiredPrefix) RequiredPrefix.Add(item);
    }
}
