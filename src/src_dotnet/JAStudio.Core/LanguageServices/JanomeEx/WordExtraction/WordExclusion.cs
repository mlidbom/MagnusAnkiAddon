using System;
using System.Collections.Generic;
using JAStudio.Core.SysUtils.Json;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;

public sealed class WordExclusion
{
   const string Secret = "aoesunth9cgrcgf";
   const int NoIndex = -1;

   public string Word { get; }
   public int Index { get; }
   readonly string _matchPart;

   WordExclusion(string word, int index, string secret)
   {
      if(secret != Secret)
      {
         throw new InvalidOperationException("please use the factory methods instead of this private constructor");
      }

      Word = word;
      Index = index;
      _matchPart = word.Split('｜')[0]; // VocabNoteQuestion.DISAMBIGUATION_MARKER
   }

   public bool ExcludesFormAtIndex(string form, int index) => form == Word && (Index == NoIndex || Index == index);

   public static WordExclusion Global(string exclusion) => new(exclusion.Trim(), NoIndex, Secret);

   public static WordExclusion AtIndex(string exclusion, int index) => new(exclusion.Trim(), index, Secret);

   /// <summary>
   /// Creates a WordExclusion from a string in the format "word:index" or "word" for global exclusions.
   /// </summary>
   public static WordExclusion FromString(string value)
   {
      var parts = value.Split(':');
      if(parts.Length == 1)
      {
         return Global(parts[0]);
      } else if(parts.Length == 2)
      {
         return AtIndex(parts[0], int.Parse(parts[1]));
      }

      throw new ArgumentException($"Invalid exclusion format: {value}");
   }

   public override bool Equals(object? obj)
   {
      if(obj is WordExclusion other)
      {
         return Word == other.Word && Index == other.Index;
      }

      return false;
   }

   public override int GetHashCode() => HashCode.Combine(Word, Index);

   public override string ToString() => $"WordExclusion('{Word}', {Index})";

   public bool ExcludesAllWordsExcludedBy(WordExclusion other) => Word == other.Word && (Index == NoIndex || Index == other.Index);

   public Dictionary<string, object> ToDict() =>
      new()
      {
         { "word", Word },
         { "index", Index }
      };

   public static WordExclusion FromReader(JsonReader reader) =>
      new(
         reader.GetString("word"),
         reader.GetInt("index"),
         Secret
      );
}
