using Avalonia.Controls;
using Avalonia.Threading;
using Compze.Utilities.Logging;
using JAStudio.Core;
using JAStudio.UI.Utils;
using JAStudio.UI.Views;

namespace JAStudio.UI;

/// <summary>
/// Factory / show methods for all application dialogs.
/// Exposed via <see cref="JAStudioAppRoot.Dialogs"/>.
/// </summary>
public class AppDialogs
{
   readonly Core.App _app;
   TemporaryServiceCollection Services => _app.Services;

   internal AppDialogs(Core.App app) => _app = app;

   /// <summary>
   /// Show a dialog and wait for it to close.
   /// </summary>
   public void ShowDialog<T>() where T : Window, new()
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var window = new T();
         window.Show();
      });
   }

   /// <summary>
   /// Show the VocabFlagsDialog for editing a vocab note's flags.
   /// </summary>
   public void ShowVocabFlagsDialog(long vocabId)
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var vocabCache = _app.Collection.Vocab;
         var vocab = vocabCache.WithExternalIdOrNone(vocabId);
         if(vocab == null)
         {
            this.Log().Info($"Vocab note with ID {vocabId} not found");
            return;
         }

         var window = new VocabFlagsDialog(vocab, Services);
         WindowPositioner.PositionNearCursor(window);
         window.Show();
      });
   }

   /// <summary>
   /// Show the VocabEditorDialog for editing a vocab note's fields.
   /// </summary>
   public void ShowVocabEditorDialog(long vocabId)
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var vocab = _app.Collection.Vocab.WithExternalIdOrNone(vocabId);
         if(vocab == null)
         {
            this.Log().Info($"Vocab note with ID {vocabId} not found");
            return;
         }

         var window = new VocabEditorDialog(vocab);
         WindowPositioner.PositionNearCursor(window);
         window.Show();
      });
   }

   /// <summary>
   /// Show the KanjiEditorDialog for editing a kanji note's fields.
   /// </summary>
   public void ShowKanjiEditorDialog(long kanjiId)
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var kanji = _app.Collection.Kanji.WithExternalIdOrNone(kanjiId);
         if(kanji == null)
         {
            this.Log().Info($"Kanji note with ID {kanjiId} not found");
            return;
         }

         var window = new KanjiEditorDialog(kanji);
         WindowPositioner.PositionNearCursor(window);
         window.Show();
      });
   }

   /// <summary>
   /// Show the SentenceEditorDialog for editing a sentence note's fields.
   /// </summary>
   public void ShowSentenceEditorDialog(long sentenceId)
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var sentence = _app.Collection.Sentences.WithExternalIdOrNone(sentenceId);
         if(sentence == null)
         {
            this.Log().Info($"Sentence note with ID {sentenceId} not found");
            return;
         }

         var window = new SentenceEditorDialog(sentence);
         WindowPositioner.PositionNearCursor(window);
         window.Show();
      });
   }

   /// <summary>
   /// Show the About dialog.
   /// </summary>
   public void ShowAboutDialog()
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var window = new AboutDialog();
         WindowPositioner.PositionNearCursor(window);
         window.Show();
      });
   }

   /// <summary>
   /// Show the Options dialog for Japanese configuration settings.
   /// </summary>
   public void ShowOptionsDialog()
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         this.Log().Info("Creating OptionsDialog window...");
         var window = new OptionsDialog(Services);
         WindowPositioner.PositionNearCursor(window);
         this.Log().Info("OptionsDialog created, calling Show()...");
         window.Show();
         this.Log().Info("OptionsDialog.Show() completed");
      });
   }

   /// <summary>
   /// Show the Readings Mappings dialog for editing readings mappings.
   /// </summary>
   public void ShowReadingsMappingsDialog()
   {
      this.Log().Info("ShowReadingsMappingsDialog() called");
      Dispatcher.UIThread.Invoke(() =>
      {
         var window = new ReadingsMappingsDialog(Services);
         WindowPositioner.PositionNearCursor(window);
         window.Show();
      });
   }

   /// <summary>
   /// Toggle the Note Search dialog visibility.
   /// Shows the dialog if hidden, hides it if visible.
   /// </summary>
   public void ToggleNoteSearchDialog()
   {
      this.Log().Info("ToggleNoteSearchDialog() called");
      Dispatcher.UIThread.Invoke(() =>
      {
         NoteSearchDialog.ToggleVisibility(Services);
      });
   }

   /// <summary>
   /// Toggle the English Word Search dialog visibility.
   /// Shows the dialog if hidden, hides it if visible.
   /// </summary>
   public void ToggleEnglishWordSearchDialog()
   {
      this.Log().Info("ToggleEnglishWordSearchDialog() called");
      Dispatcher.UIThread.Invoke(EnglishWordSearchDialog.ToggleVisibility);
   }
}
