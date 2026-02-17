using System;
using System.Collections.Generic;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using JAStudio.Core.Note;
using JAStudio.UI.ViewModels;

namespace JAStudio.UI.Views;

public partial class MissingFilesDialog : Window
{
   readonly Action<NoteId>? _openNote;

   public MissingFilesDialog() => InitializeComponent();

   public MissingFilesDialog(List<MissingFileRow> vocabRows, List<MissingFileRow> sentenceRows, List<MissingFileRow> kanjiRows, Action<NoteId> openNote) : this()
   {
      _openNote = openNote;

      VocabGrid.ItemsSource = vocabRows;
      SentenceGrid.ItemsSource = sentenceRows;
      KanjiGrid.ItemsSource = kanjiRows;

      VocabTab.Header = $"Vocab ({vocabRows.Count})";
      SentenceTab.Header = $"Sentences ({sentenceRows.Count})";
      KanjiTab.Header = $"Kanji ({kanjiRows.Count})";

      VocabGrid.DoubleTapped += OnGridDoubleTapped;
      SentenceGrid.DoubleTapped += OnGridDoubleTapped;
      KanjiGrid.DoubleTapped += OnGridDoubleTapped;
   }

   void OnGridDoubleTapped(object? sender, TappedEventArgs e)
   {
      if(sender is DataGrid grid && grid.SelectedItem is MissingFileRow row)
         _openNote?.Invoke(row.NoteId);
   }

   void OnCloseClick(object? sender, RoutedEventArgs e) => Close();
}
