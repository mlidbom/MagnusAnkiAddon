using System;
using JAStudio.Core.Note;

namespace JAStudio.Core.Note.Sentences.Serialization;

public class ParsedWordSerializer
{
    public static readonly string Separator = $" {StringExtensions.InvisibleSpace} ";

    public static string ToRow(ParsedMatch parsedWord)
    {
        return string.Join(Separator, new[]
        {
            parsedWord.Variant,
            parsedWord.StartIndex.ToString(),
            parsedWord.IsDisplayed ? "1" : "0",
            parsedWord.ParsedForm,
            parsedWord.VocabId?.Value.ToString() ?? ""
        });
    }

    public static ParsedMatch FromRow(string serialized)
    {
        var values = serialized.Split(new[] { Separator }, System.StringSplitOptions.None);

        // Parse VocabId: supports both Guid format (new) and legacy long format
        NoteId? vocabId;
        var idStr = values[4];
        if(Guid.TryParse(idStr, out var guid) && guid != Guid.Empty)
        {
            vocabId = new NoteId(guid);
        }
        else if(long.TryParse(idStr, out var legacyId) && legacyId != -1)
        {
            // Legacy long ID — generate deterministic Guid matching NoteBulkLoader
            vocabId = new NoteId(NoteId.DeterministicGuidFromAnkiId(legacyId));
        }
        else
        {
            vocabId = null;
        }

        return new ParsedMatch(
            values[0],
            int.Parse(values[1]),
            values[2] != "0",
            values[3],
            vocabId
        );
    }
}
