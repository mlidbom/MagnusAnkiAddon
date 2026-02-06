using System;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Tests.Fixtures.BaseData.SampleData;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core.Tests.Fixtures;

public enum DataNeeded
{
   Kanji = 2,
   Vocabulary = 4,
   Sentences = 8,
   All = Kanji | Vocabulary | Sentences
}

public static class CollectionFactory
{
   public static IDisposable InjectEmptyCollection()
   {
      TestApp.Reset();
      return new CollectionScope();
   }

   public static IDisposable InjectCollectionWithSelectData(DataNeeded data)
   {
      TestApp.Reset();

      if(data.HasFlag(DataNeeded.Kanji))
      {
         foreach(var kanjiSpec in KanjiSpec.TestKanjiList)
         {
            KanjiNote.Create(kanjiSpec.Question, kanjiSpec.Answer, kanjiSpec.OnReadings, kanjiSpec.KunReading);
         }
      }

      if(data.HasFlag(DataNeeded.Vocabulary))
      {
         foreach(var vocab in VocabLists.TestSpecialVocab)
         {
            vocab.CreateVocabNote();
         }
      }

      if(data.HasFlag(DataNeeded.Sentences))
      {
         foreach(var sentence in SentenceSpec.TestSentenceList)
         {
            SentenceNote.CreateTestNote(sentence.Question, sentence.Answer);
         }
      }

      return new CollectionScope();
   }

   private class CollectionScope : IDisposable
   {
      public void Dispose()
      {
         // No cleanup needed - next test will call Reset()
      }
   }
}
