using System.Collections.Frozen;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.Vocabulary;
using Wacton.Desu.Enums;
using Wacton.Desu.Japanese;
using NameEntry = Wacton.Desu.Names.INameEntry;

namespace JAStudio.Core.LanguageServices.JamdictEx;

public class SenseEX
{
   public List<string> Glosses { get; }
   public FrozenSet<string> Pos { get; }
   public bool IsKanaOnly { get; }

   internal SenseEX(ISense source, IEnumerable<PartOfSpeech>? inheritedPos = null)
   {
      Glosses = source.Glosses
                      .Where(g => g.Language.Equals(Language.English))
                      .Select(g => g.Term.Replace(" ", "-"))
                      .ToList();

      var pos = source.PartsOfSpeech.ToList();
      if(!pos.Any() && inheritedPos != null)
         pos = inheritedPos.ToList();

      var posList = pos.Select(p => p.Code).ToList();
      Pos = POSSetManager.InternAndHarmonizeFromList(posList);

      IsKanaOnly = source.Miscellanea.Any(m => m.Code == Miscellaneous.UsuallyKanaAlone.Code);
   }

   internal SenseEX(Wacton.Desu.Names.ITranslation source)
   {
      Glosses = source.Transcriptions
                      .Select(t => t.Replace(" ", "-"))
                      .ToList();

      Pos = FrozenSet<string>.Empty;
      IsKanaOnly = false;
   }

   public bool IsTransitiveVerb() => POSSetManager.IsTransitiveVerb(Pos);
   public bool IsIntransitiveVerb() => POSSetManager.IsIntransitiveVerb(Pos);

   bool AllGlossesStartWith(string prefix) => Glosses.All(it => it.StartsWith(prefix));

   public bool IsToBeVerb() => AllGlossesStartWith("to-be-");

   public string FormatGlosses()
   {
      if(POSSetManager.IsVerb(Pos))
      {
         var typeMarker = "{?}";
         if(IsTransitiveVerb()) typeMarker = "{}";
         if(IsIntransitiveVerb()) typeMarker = ":";

         var startGroup = "{";
         var endGroup = "}";
         if(Glosses.Count == 1)
         {
            startGroup = "";
            endGroup = "";
         }

         if(IsToBeVerb())
         {
            return $"to-be:{startGroup}{string.Join("/", Glosses.Select(it => RemovePrefix(it, "to-be-")))}{endGroup}";
         }

         if(AllGlossesStartWith("to-"))
         {
            return $"to{typeMarker}{startGroup}{string.Join("/", Glosses.Select(it => RemovePrefix(it, "to-")))}{endGroup}";
         }
      }

      return string.Join("/", Glosses);
   }

   static string RemovePrefix(string text, string prefix) => text.StartsWith(prefix) ? text.Substring(prefix.Length) : text;
}

public class KanaFormEX
{
   public string Text { get; }
   public List<string> PriorityTags { get; }

   internal KanaFormEX(IReading source)
   {
      Text = source.Text;
      PriorityTags = source.Priorities.Select(p => p.Code).ToList();
   }

   internal KanaFormEX(Wacton.Desu.Names.IReading source)
   {
      Text = source.Text;
      PriorityTags = source.Priorities.Select(p => p.Code).ToList();
   }
}

public class KanjiFormEX
{
   public string Text { get; }
   public List<string> PriorityTags { get; }

   internal KanjiFormEX(IKanji source)
   {
      Text = source.Text;
      PriorityTags = source.Priorities.Select(p => p.Code).ToList();
   }

   internal KanjiFormEX(Wacton.Desu.Names.IKanji source)
   {
      Text = source.Text;
      PriorityTags = source.Priorities.Select(p => p.Code).ToList();
   }
}

public sealed class DictEntry
{
   public List<KanaFormEX> KanaForms { get; }
   public List<KanjiFormEX> KanjiForms { get; }
   public List<SenseEX> Senses { get; }

   DictEntry(List<KanaFormEX> kanaForms, List<KanjiFormEX> kanjiForms, List<SenseEX> senses)
   {
      KanaForms = kanaForms;
      KanjiForms = kanjiForms;
      Senses = senses;
   }

   internal static DictEntry FromDesu(IJapaneseEntry source)
   {
      var senses = new List<SenseEX>();
      IEnumerable<PartOfSpeech> lastPos = [];

      foreach(var sense in source.Senses)
      {
         var currentPos = sense.PartsOfSpeech.ToList();
         if(currentPos.Any())
            lastPos = currentPos;

         var senseEx = new SenseEX(sense, lastPos);
         if(senseEx.Glosses.Any())
            senses.Add(senseEx);
      }

      return new(source.Readings.Select(r => new KanaFormEX(r)).ToList(),
                 source.Kanjis.Select(k => new KanjiFormEX(k)).ToList(),
                 senses);
   }

   internal static DictEntry FromDesuName(NameEntry source) =>
      new(source.Readings.Select(r => new KanaFormEX(r)).ToList(),
          source.Kanjis.Select(k => new KanjiFormEX(k)).ToList(),
          source.Translations.Select(t => new SenseEX(t)).ToList());

   public List<string> KanaFormsText() => KanaForms.Select(it => it.Text).ToList();
   public List<string> KanjiFormsText() => KanjiForms.Select(it => it.Text).ToList();

   public bool IsKanaOnly()
   {
      return !KanjiForms.Any() || Senses.Any(sense => sense.IsKanaOnly);
   }

   public bool HasMatchingKanaForm(string search)
   {
      search = KanaUtils.KatakanaToHiragana(search);
      return KanaForms.Any(form => search == KanaUtils.KatakanaToHiragana(form.Text));
   }

   public bool HasMatchingKanjiForm(string search)
   {
      search = KanaUtils.KatakanaToHiragana(search);
      return KanjiForms.Any(form => search == KanaUtils.KatakanaToHiragana(form.Text));
   }

   public HashSet<string> ValidForms(bool forceAllowKanaOnly = false)
   {
      var kanaSet = KanaFormsText().ToHashSet();
      var kanjiSet = KanjiFormsText().ToHashSet();

      if(IsKanaOnly() || forceAllowKanaOnly)
      {
         kanaSet.UnionWith(kanjiSet);
         return kanaSet;
      }

      return kanjiSet;
   }

   public bool IsTransitiveVerb() => Senses.All(it => it.IsTransitiveVerb());
   public bool IsIntransitiveVerb() => Senses.All(it => it.IsIntransitiveVerb());
   public bool IsToBeVerb() => Senses.All(it => it.IsToBeVerb());

   public HashSet<string> PartsOfSpeech()
   {
      var result = new HashSet<string>();
      foreach(var sense in Senses)
      {
         result.UnionWith(sense.Pos);
      }

      return result;
   }

   public string FormatAnswer()
   {
      var defaultFormat = string.Join(" | ", Senses.Select(it => it.FormatGlosses()));

      if(IsToBeVerb())
      {
         return $"to-be: {defaultFormat.Replace("to-be:", "").Replace("{", "").Replace("}", "")}";
      }

      if(IsTransitiveVerb())
      {
         return $"to{{}} {defaultFormat.Replace("to{}", "").Replace("{", "").Replace("}", "")}";
      }

      if(IsIntransitiveVerb())
      {
         if(defaultFormat.Contains("to-be:"))
         {
            return $"to: {defaultFormat.Replace("to-be:", "be-").Replace("to:", "")}";
         } else
         {
            return $"to: {defaultFormat.Replace("to:", "").Replace("{", "").Replace("}", "")}";
         }
      }

      return defaultFormat;
   }
}
