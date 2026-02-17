using Avalonia.Threading;
using Compze.Utilities.Logging;
using JAStudio.Core;
using JAStudio.UI.Utils;
using JAStudio.UI.Views;

namespace JAStudio.UI;

public class AppDialogs
{
   readonly CoreApp _coreApp;
   TemporaryServiceCollection Services => _coreApp.Services;

   internal AppDialogs(CoreApp coreApp) => _coreApp = coreApp;

   internal void ShowOptionsDialog()
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         this.Log().Info("Creating OptionsDialog window...");
         var window = new OptionsDialog(Services);
         window.PositionNearCursor();
         this.Log().Info("OptionsDialog created, calling Show()...");
         window.Show();
         this.Log().Info("OptionsDialog.Show() completed");
      });
   }

   internal void ShowReadingsMappingsDialog()
   {
      this.Log().Info("ShowReadingsMappingsDialog() called");
      Dispatcher.UIThread.Invoke(() =>
      {
         var window = new ReadingsMappingsDialog(Services);
         window.PositionNearCursor();
         window.Show();
      });
   }

   // ReSharper disable once MemberCanBeInternal used from python
   public void ToggleNoteSearchDialog()
   {
      this.Log().Info("ToggleNoteSearchDialog() called");
      Dispatcher.UIThread.Invoke(() =>
      {
         NoteSearchDialog.ToggleVisibility(Services);
      });
   }

   // ReSharper disable once UnusedMember.Global - Called from Python (global_shortcuts.py)
   public void ToggleEnglishWordSearchDialog()
   {
      this.Log().Info("ToggleEnglishWordSearchDialog() called");
      Dispatcher.UIThread.Invoke(EnglishWordSearchDialog.ToggleVisibility);
   }
}
