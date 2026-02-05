using JAStudio.Core.Note.NoteFields;
using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Sentences.Serialization;

public class ParsingResultSerializer : IObjectSerializer<ParsingResult>
{
    private static readonly string NewlineReplacement = $"NEWLINE{StringExtensions.InvisibleSpace}";

    public ParsingResult Deserialize(string serialized)
    {
        var rows = serialized.Split('\n');
        if (rows.Length < 2)
        {
            return new ParsingResult(new List<ParsedMatch>(), "", "");
        }

        try
        {
            if (string.IsNullOrEmpty(serialized))
            {
                return new ParsingResult(new List<ParsedMatch>(), "", "");
            }

            var parsedWords = rows.Skip(2)
                .Select(row => ParsedWordSerializer.FromRow(row))
                .ToList();

            return new ParsingResult(
                parsedWords,
                RestoreNewline(rows[1]),
                rows[0]
            );
        }
        catch (Exception ex)
        {
            MyLog.Warning($"Failed to deserialize ParsingResult:\nmessage:\n{ex.Message}\n{serialized}");
            return new ParsingResult(new List<ParsedMatch>(), "", "");
        }
    }

    private string ReplaceNewline(string value)
    {
        return value.Replace("\n", NewlineReplacement);
    }

    private string RestoreNewline(string serializedValue)
    {
        return serializedValue.Replace(NewlineReplacement, "\n");
    }

    public string Serialize(ParsingResult instance)
    {
        var lines = new List<string>
        {
            instance.ParserVersion,
            ReplaceNewline(instance.Sentence)
        };

        lines.AddRange(instance.ParsedWords.Select(word => ParsedWordSerializer.ToRow(word)));

        return string.Join("\n", lines);
    }
}
