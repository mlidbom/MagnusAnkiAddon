using System;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Tests.Fixtures.BaseData.SampleData;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core.Tests.Fixtures;

public enum DataNeeded
{
   None = 0,
   Kanji = 2,
   Vocabulary = 4,
   Sentences = 8,
   All = Kanji | Vocabulary | Sentences
}

public static class CollectionFactory
{
   public static IDisposable InjectCollectionWithSelectData(DataNeeded data)
   {
      TestApp.Reset();
      if(data == DataNeeded.None)
         return new CollectionScope();

      var noteServices = TemporaryServiceCollection.Instance.NoteServices;

      if(data.HasFlag(DataNeeded.Kanji))
      {
         foreach(var kanjiSpec in KanjiSpec.TestKanjiList)
         {
            KanjiNote.Create(noteServices, kanjiSpec.Question, kanjiSpec.Answer, kanjiSpec.OnReadings, kanjiSpec.KunReading);
         }
      }

      if(data.HasFlag(DataNeeded.Vocabulary))
      {
         foreach(var vocab in VocabLists.TestSpecialVocab)
         {
            TemporaryServiceCollection.Instance.VocabNoteFactory.Create(vocab.DisambiguationName, vocab.Answer, vocab.Readings, vocab.InitializeNote);
         }
      }

      if(data.HasFlag(DataNeeded.Sentences))
      {
         foreach(var sentence in SentenceSpec.TestSentenceList)
         {
            SentenceNote.CreateTestNote(noteServices, sentence.Question, sentence.Answer);
         }
      }

      return new CollectionScope();
   }

   class CollectionScope : IDisposable
   {
      public void Dispose()
      {
         // No cleanup needed - next test will call Reset()
      }
   }
}
