using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Storage.Media;

public class MediaImportRuleSet
{
   readonly List<VocabImportRule> _vocabRules;
   readonly List<SentenceImportRule> _sentenceRules;
   readonly List<KanjiImportRule> _kanjiRules;

   public MediaImportRuleSet(
      List<VocabImportRule> vocabRules,
      List<SentenceImportRule> sentenceRules,
      List<KanjiImportRule> kanjiRules)
   {
      _vocabRules = vocabRules.OrderByDescending(r => r.Prefix.Segments.Count).ToList();
      _sentenceRules = sentenceRules.OrderByDescending(r => r.Prefix.Segments.Count).ToList();
      _kanjiRules = kanjiRules.OrderByDescending(r => r.Prefix.Segments.Count).ToList();
   }

   public VocabImportRule? TryResolveVocab(SourceTag sourceTag, VocabMediaField field) =>
      _vocabRules.FirstOrDefault(r => r.Field == field && sourceTag.IsContainedIn(r.Prefix));

   public SentenceImportRule? TryResolveSentence(SourceTag sourceTag, SentenceMediaField field) =>
      _sentenceRules.FirstOrDefault(r => r.Field == field && sourceTag.IsContainedIn(r.Prefix));

   public KanjiImportRule? TryResolveKanji(SourceTag sourceTag, KanjiMediaField field) =>
      _kanjiRules.FirstOrDefault(r => r.Field == field && sourceTag.IsContainedIn(r.Prefix));
}
