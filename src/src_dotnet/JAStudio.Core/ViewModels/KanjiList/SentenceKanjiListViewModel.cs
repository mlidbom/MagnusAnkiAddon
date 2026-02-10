using JAStudio.Core.Note.Collection;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.ViewModels.KanjiList;

public class SentenceKanjiListViewModel
{
   readonly KanjiCollection _kanji;
   internal SentenceKanjiListViewModel(KanjiCollection kanji) => _kanji = kanji;

    public KanjiListViewModel Create(List<string> kanji)
    {
        var kanjiNotes = _kanji.WithAnyKanjiIn(kanji);
        var kanjiViewModels = kanjiNotes.Select(note => new KanjiViewModel(note)).ToList();
        return new KanjiListViewModel(kanjiViewModels);
    }
}
