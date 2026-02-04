using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.ViewModels.KanjiList;

public static class SentenceKanjiListViewModel
{
    public static KanjiListViewModel Create(List<string> kanji)
    {
        var kanjiNotes = App.Col().Kanji.WithAnyKanjiIn(kanji);
        var kanjiViewModels = kanjiNotes.Select(note => new KanjiViewModel(note)).ToList();
        return new KanjiListViewModel(kanjiViewModels);
    }
}
