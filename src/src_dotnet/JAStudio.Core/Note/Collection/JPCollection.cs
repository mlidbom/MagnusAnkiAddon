namespace JAStudio.Core.Note.Collection;

public class JPCollection
{
   public VocabCollection Vocab { get; }
   public KanjiCollection Kanji { get; }
   public SentenceCollection Sentences { get; }

   public JPCollection(IBackendNoteCreator backendNoteCreator)
   {
      MyLog.Info("JPCollection.__init__");

      Vocab = new VocabCollection(backendNoteCreator);
      Kanji = new KanjiCollection(backendNoteCreator);
      Sentences = new SentenceCollection(backendNoteCreator);
   }

   public void SetNoteServices(NoteServices noteServices)
   {
      Vocab.Cache.SetNoteServices(noteServices);
      Kanji.Cache.SetNoteServices(noteServices);
      Sentences.Cache.SetNoteServices(noteServices);
   }
}
