using System;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Tests.Fixtures;
using JAStudio.Core.ViewModels.KanjiList;
using Xunit;

namespace JAStudio.Core.Tests.ViewModels;

/// <summary>
/// Tests ported from test_kanji_list_viewmodel.py
/// </summary>
public class KanjiListViewModelTests : IDisposable
{
    private readonly IDisposable _collectionScope;

    public KanjiListViewModelTests()
    {
        _collectionScope = CollectionFactory.InjectCollectionWithAllSampleData();
    }

    public void Dispose()
    {
        _collectionScope.Dispose();
    }

    [Fact]
    public void KanjiListViewModel()
    {
        var sentences = App.Col().Sentences.All();
        foreach (var sentence in sentences)
        {
            var extractedKanji = sentence.ExtractKanji();
            var viewModel = SentenceKanjiListViewModel.Create(extractedKanji);

            var extractedKanjiSet = extractedKanji.ToHashSet();
            var foundKanjiSet = viewModel.KanjiList.Select(m => m.Question()).ToHashSet();

            Assert.Equal(extractedKanjiSet, foundKanjiSet);
        }
    }
}
