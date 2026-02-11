using Avalonia.Threading;
using JAStudio.Core;
using JAStudio.PythonInterop;
using JAStudio.UI.Menus;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Views;

namespace JAStudio.UI;

/// <summary>
/// Factory methods for building menus (context menus, toolbar menus, browser menus).
/// Exposed via <see cref="JAStudioAppRoot.Menus"/>.
/// </summary>
public class AppMenus
{
   readonly TemporaryServiceCollection _services;
   readonly AppDialogs _dialogs;

   internal AppMenus(TemporaryServiceCollection services, AppDialogs dialogs)
   {
      _services = services;
      _dialogs = dialogs;
   }

   /// <summary>Called from Python to build right-click context menus.</summary>
   public NoteContextMenu CreateNoteContextMenu() => new(_services);

   /// <summary>Called from Python to build the main "Japanese" tools menu.</summary>
   public JapaneseMainMenu CreateJapaneseMainMenu() => new(_services, _dialogs);

   /// <summary>
   /// Show the context menu popup at the current cursor position.
   /// </summary>
   public void ShowContextMenuPopup(string clipboardContent, string selectionContent, int x, int y)
   {
      Dispatcher.UIThread.Invoke(() =>
      {
         var menuControl = new ContextMenuPopup(clipboardContent ?? "", selectionContent ?? "");
         menuControl.ShowAt(x, y);
      });
   }

   /// <summary>
   /// Build browser context menu specification.
   /// Returns UI-agnostic menu specs that Python can convert to PyQt menus.
   /// </summary>
   public SpecMenuItem BuildBrowserMenuSpec(
      dynamic selectedCardIds,
      dynamic selectedNoteIds) =>
      new BrowserMenus(_services).BuildBrowserMenuSpec(PythonDotNetShim.LongList.ToDotNet(selectedCardIds),
                                                       PythonDotNetShim.LongList.ToDotNet(selectedNoteIds));
}
