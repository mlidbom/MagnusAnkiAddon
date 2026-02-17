using System.Linq;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.ViewModels.KanjiList;
using Xunit;

namespace JAStudio.Core.Tests.ViewModels;

/// <summary>
/// Tests ported from test_kanji_list_viewmodel.py
/// </summary>
public class KanjiListViewModelTests : SpecificationUsingACollection
{
   [Fact]
   public void KanjiListViewModel()
   {
      var sentences = GetService<SentenceCollection>().All();
      foreach(var sentence in sentences)
      {
         var extractedKanji = sentence.ExtractKanji();
         var viewModel = GetService<SentenceKanjiListViewModel>().Create(extractedKanji);

         var extractedKanjiSet = extractedKanji.ToHashSet();
         var foundKanjiSet = viewModel.KanjiList.Select(m => m.Question()).ToHashSet();

         Assert.Equal(extractedKanjiSet, foundKanjiSet);
      }
   }
}
