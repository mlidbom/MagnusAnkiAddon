using System;

namespace JAStudio.Core.Note.Sentences.Serialization;

public class ParsedWordSerializer
{
   static readonly string Separator = $" {StringExtensions.InvisibleSpace} ";

   public static string ToRow(ParsedMatch parsedWord)
   {
      return string.Join(Separator,
                         new[]
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
      var values = serialized.Split([Separator], StringSplitOptions.None);

      // Parse VocabId: supports both Guid format (new) and legacy long format
      NoteId? vocabId;
      var idStr = values[4];
      if(Guid.TryParse(idStr, out var guid) && guid != Guid.Empty)
      {
         vocabId = new VocabId(guid);
      } else if(long.TryParse(idStr, out _) && idStr != "-1")
      {
         // Legacy long Anki ID from before GUID migration — cannot resolve.
         // Will be re-resolved when the sentence is next parsed.
         vocabId = null;
      } else
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
