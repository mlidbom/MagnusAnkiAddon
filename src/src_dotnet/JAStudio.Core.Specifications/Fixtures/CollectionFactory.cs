using System;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Specifications.Fixtures.BaseData.SampleData;

namespace JAStudio.Core.Specifications.Fixtures;

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
   public static AppScope InjectCollectionWithSelectData(DataNeeded data)
   {
      var app = AppBootstrapper.BootstrapForTests();
      if(data == DataNeeded.None)
         return new AppScope(app);

      var noteServices = app.Services.NoteServices;

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
            app.Services.VocabNoteFactory.Create(vocab.DisambiguationName, vocab.Answer, vocab.Readings, vocab.InitializeNote);
         }
      }

      if(data.HasFlag(DataNeeded.Sentences))
      {
         foreach(var sentence in SentenceSpec.TestSentenceList)
         {
            SentenceNote.CreateTestNote(noteServices, sentence.Question, sentence.Answer);
         }
      }

      return new AppScope(app);
   }

   public class AppScope(CoreApp coreApp) : IDisposable
   {
      public CoreApp CoreApp { get; } = coreApp;

      public void Dispose()
      {
         CoreApp.Dispose();
      }
   }
}
