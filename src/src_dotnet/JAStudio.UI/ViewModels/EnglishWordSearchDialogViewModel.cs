using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using CommunityToolkit.Mvvm.ComponentModel;
using JAStudio.Core.LanguageServices.EnglishDictionary;
using JAStudio.UI.Utils;

namespace JAStudio.UI.ViewModels;

public partial class EnglishWordSearchDialogViewModel : ObservableObject
{
   private const int MaxResults = 100;

   [ObservableProperty]
   private string _searchText = string.Empty;

   [ObservableProperty]
   private EnglishWordResultViewModel? _selectedResult;

   public ObservableCollection<EnglishWordResultViewModel> Results { get; } = new();

   partial void OnSearchTextChanged(string value)
   {
      PerformSearch();
   }

   private void PerformSearch()
   {
      var searchText = SearchText.Trim();
      Results.Clear();

      if(string.IsNullOrWhiteSpace(searchText))
      {
         return;
      }

      var results = SearchEnglishWords(searchText);
      foreach(var result in results)
      {
         Results.Add(result);
      }
   }

   private List<EnglishWordResultViewModel> SearchEnglishWords(string searchText)
   {
      var dictionary = EnglishDictionary.Instance;
      var matchingWords = dictionary.WordsContainingStartingWithFirstThenByShortestFirst(searchText);

      return matchingWords
            .Take(MaxResults)
            .Select(word =>
             {
                var definition = word.Senses.Count > 0 ? word.Senses[0].Definition : "no definition";
                return new EnglishWordResultViewModel(word.Word, definition);
             })
            .ToList();
   }

   public void OpenInMerriamWebster()
   {
      if(SelectedResult == null)
         return;

      var url = $"https://www.merriam-webster.com/dictionary/{SelectedResult.Word}";
      BrowserLauncher.OpenUrl(url);
   }

   public void OpenInGoogle()
   {
      if(SelectedResult == null)
         return;

      var url = $"https://www.google.com/search?q=define+{SelectedResult.Word}";
      BrowserLauncher.OpenUrl(url);
   }

   public void OpenInOED()
   {
      if(SelectedResult == null)
         return;

      var url = $"https://www.oed.com/search/dictionary/?scope=Entries&q={SelectedResult.Word}";
      BrowserLauncher.OpenUrl(url);
   }
}

public class EnglishWordResultViewModel
{
   public string Word { get; }
   public string Definition { get; }

   public EnglishWordResultViewModel(string word, string definition)
   {
      Word = word;
      Definition = definition;
   }
}
