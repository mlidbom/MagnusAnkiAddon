using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

static class VocabNoteSorting
{
   public static List<VocabNote> SortVocabListByStudyingStatus(
      IEnumerable<VocabNote> vocabs,
      List<string>? primaryVoc = null,
      string? preferredKanji = null)
   {
      var primaryVocList = primaryVoc ?? new List<string>();

      int PreferPrimaryVocabInOrder(VocabNote localVocab)
      {
         for(var index = 0; index < primaryVocList.Count; index++)
         {
            var primary = primaryVocList[index];
            var readings = localVocab.GetReadings();

            if(localVocab.GetQuestion() == primary ||
               localVocab.Question.WithoutNoiseCharacters == primary ||
               (readings.Any() && readings[0] == primary))
            {
               return index;
            }
         }

         return 1000;
      }

      int PreferVocabWithKanji(VocabNote localVocab) => (preferredKanji == null || localVocab.GetQuestion().Contains(preferredKanji)) ? 0 : 1;

      int PreferMoreSentences(VocabNote localVocab) => -localVocab.Sentences.All().Count;

      var result = vocabs.OrderBy(v => PreferVocabWithKanji(v))
                         .ThenBy(v => PreferPrimaryVocabInOrder(v))
                         .ThenBy(v => PreferMoreSentences(v))
                         .ThenBy(v => v.GetQuestion())
                         .ToList();

      return result;
   }
}
