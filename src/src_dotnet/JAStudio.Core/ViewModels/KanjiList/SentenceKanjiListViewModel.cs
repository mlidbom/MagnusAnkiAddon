using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.ViewModels.KanjiList;

public class SentenceKanjiListViewModel
{
   readonly TemporaryServiceCollection _services;
   internal SentenceKanjiListViewModel(TemporaryServiceCollection services) => _services = services;

    public KanjiListViewModel Create(List<string> kanji)
    {
        var kanjiNotes = TemporaryServiceCollection.Instance.App.Col().Kanji.WithAnyKanjiIn(kanji);
        var kanjiViewModels = kanjiNotes.Select(note => new KanjiViewModel(note)).ToList();
        return new KanjiListViewModel(kanjiViewModels);
    }
}
