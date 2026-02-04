using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Utilities;

namespace JAStudio.Core.Note.Sentences.Serialization;

public class SentenceConfigurationSerializer
{
    private static string _emptyObjectJson = "";
    private static readonly SentenceConfigurationSerializer _instance = new();

    public static SentenceConfigurationSerializer Instance => _instance;

    private SentenceConfigurationSerializer()
    {
        if (string.IsNullOrEmpty(_emptyObjectJson))
        {
            _emptyObjectJson = Serialize(Deserialize("", () => { }));
        }
    }

    public SentenceConfiguration Deserialize(string json, Action saveCallback)
    {
        if (string.IsNullOrEmpty(json))
        {
            return new SentenceConfiguration(
                new List<string>(),
                WordExclusionSet.Empty(saveCallback),
                WordExclusionSet.Empty(saveCallback)
            );
        }

        var dictData = JsonHelper.JsonToDict(json);
        var reader = new JsonReader(dictData);
        return new SentenceConfiguration(
            reader.GetStringList("highlighted_words", new List<string>()),
            new WordExclusionSet(saveCallback, reader.GetObjectList("incorrect_matches", r => WordExclusion.FromReader(r), new List<WordExclusion>())),
            new WordExclusionSet(saveCallback, reader.GetObjectList("hidden_matches", r => WordExclusion.FromReader(r), new List<WordExclusion>()))
        );
    }

    public string Serialize(SentenceConfiguration config)
    {
        var jsonDict = new Dictionary<string, object>();
        
        if (config.HighlightedWords.Any())
        {
            jsonDict["highlighted_words"] = config.HighlightedWords.ToList();
        }
        
        if (config.IncorrectMatches.Words().Any())
        {
            jsonDict["incorrect_matches"] = config.IncorrectMatches.Get().Select(e => e.ToDict()).ToList();
        }
        
        if (config.HiddenMatches.Get().Any())
        {
            jsonDict["hidden_matches"] = config.HiddenMatches.Get().Select(e => e.ToDict()).ToList();
        }

        var json = JsonHelper.DictToJson(jsonDict);
        return json != _emptyObjectJson ? json : "";
    }
}
