using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage;

public class AllNotesData
{
    public List<KanjiNote> Kanji { get; }
    public List<VocabNote> Vocab { get; }
    public List<SentenceNote> Sentences { get; }

    public AllNotesData(List<KanjiNote> kanji, List<VocabNote> vocab, List<SentenceNote> sentences)
    {
        Kanji = kanji.OrderBy(n => n.GetId().Value).ToList();
        Vocab = vocab.OrderBy(n => n.GetId().Value).ToList();
        Sentences = sentences.OrderBy(n => n.GetId().Value).ToList();
    }
}
