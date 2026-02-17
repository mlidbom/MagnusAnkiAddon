using Avalonia.Threading;
using Compze.Utilities.Logging;
using JAStudio.Core;
using JAStudio.UI.Utils;
using JAStudio.UI.Views;

namespace JAStudio.UI;

public class AnkiDialogs
{
   readonly CoreApp _coreApp;
   TemporaryServiceCollection Services => _coreApp.Services;

   internal AnkiDialogs(CoreApp coreApp) => _coreApp = coreApp;

   // ReSharper disable once MemberCanBeInternal used from python
   // ReSharper disable once UnusedMember.Global used from python
   internal void ShowReadingsMappingsDialog()
   {
      this.Log().Info("ShowReadingsMappingsDialog() called");
      Dispatcher.UIThread.Invoke(() => new ReadingsMappingsDialog(Services).ShowNearCursor());
   }

   // ReSharper disable once MemberCanBeInternal used from python
   // ReSharper disable once UnusedMember.Global used from python
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
