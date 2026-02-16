using System.Collections.Generic;
using Avalonia.Controls;
using Avalonia.Interactivity;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class MissingFilesDialog : Window
{
   public MissingFilesDialog() => InitializeComponent();

   public MissingFilesDialog(List<MissingFileRow> vocabRows, List<MissingFileRow> sentenceRows, List<MissingFileRow> kanjiRows) : this()
   {
      VocabGrid.ItemsSource = vocabRows;
      SentenceGrid.ItemsSource = sentenceRows;
      KanjiGrid.ItemsSource = kanjiRows;

      VocabTab.Header = $"Vocab ({vocabRows.Count})";
      SentenceTab.Header = $"Sentences ({sentenceRows.Count})";
      KanjiTab.Header = $"Kanji ({kanjiRows.Count})";
   }

   void OnCloseClick(object? sender, RoutedEventArgs e) => Close();
}
