using JAStudio.Core.Note.CorpusData;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMetaData
{
   readonly VocabNote _vocab;
   readonly NoteGuard _guard;
   int _sentenceCount;

   public VocabNoteMetaData(VocabNote vocab, VocabData? data, NoteGuard guard)
   {
      _vocab = vocab;
      _guard = guard;
      _sentenceCount = data?.SentenceCount ?? 0;
   }

   public int SentenceCount => _sentenceCount;

   public void SetSentenceCount(int value) => _guard.Update(() => _sentenceCount = value);

   public string MetaTagsHtml(bool displayExtendedSentenceStatistics = true, bool noSentenceStatistics = false) => VocabNoteMetaTagFormatter.GetMetaTagsHtml(_vocab, displayExtendedSentenceStatistics, noSentenceStatistics);
}
