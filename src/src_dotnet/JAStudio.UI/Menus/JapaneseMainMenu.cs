using System;
using System.Collections.Generic;
using Compze.Utilities.Logging;
using JAStudio.Anki;
using JAStudio.Core.TaskRunners;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;
using JAStudio.UI.Utils;

namespace JAStudio.UI.Menus;

/// <summary>
/// Builds the main "Japanese" menu for Anki.
/// This will replace the Python menu in tools_menu.py.
/// Now uses UI-agnostic MenuItem specifications and AnkiFacade for Anki calls.
/// </summary>
public class JapaneseMainMenu
{
   readonly Core.TemporaryServiceCollection _services;
   readonly AppDialogs _dialogs;
   readonly OpenInAnkiMenus _openInAnkiMenus;

   public JapaneseMainMenu(Core.TemporaryServiceCollection services, AppDialogs dialogs)
   {
      _services = services;
      _dialogs = dialogs;
      _openInAnkiMenus = new OpenInAnkiMenus(_services);
   }

   public List<SpecMenuItem> BuildMenuSpec(Func<string> getClipboardContent) =>
   [
      BuildConfigMenuSpec(),
      BuildLookupMenuSpec(getClipboardContent),
      BuildLocalActionsMenuSpec()
   ];

   SpecMenuItem BuildConfigMenuSpec() =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home1("Config"),
         new List<SpecMenuItem>
         {
            SpecMenuItem.Command(ShortcutFinger.Home1("Options (Ctrl+Shift+S)"), OnOptions),
            SpecMenuItem.Command(ShortcutFinger.Home2("Readings mappings (Ctrl+Shift+M)"), OnReadingsMappings)
         }
      );

   SpecMenuItem BuildLookupMenuSpec(Func<string> getClipboardContent) =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home2("Lookup"),
         new List<SpecMenuItem>
         {
            SpecMenuItem.Command(ShortcutFinger.Home1("Open note (Ctrl+O)"), OnOpenNote),
            _openInAnkiMenus.BuildOpenInAnkiMenuSpec(getClipboardContent),
            WebSearchMenus.BuildWebSearchMenuSpec(getClipboardContent)
         }
      );

   SpecMenuItem BuildLocalActionsMenuSpec() =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home3("Local Actions"),
         new List<SpecMenuItem>
         {
            BuildUpdateSubmenuSpec(),
            SpecMenuItem.Command(ShortcutFinger.Home2("Convert Immersion Kit sentences"), () => BackgroundTaskManager.Run(() => AnkiFacade.Batches.ConvertImmersionKitSentences())),
            SpecMenuItem.Command(ShortcutFinger.Home3("Update everything except reanalysing sentences"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.UpdateAll())),
            SpecMenuItem.Command(ShortcutFinger.Home4("Create vocab notes for parsed words"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.CreateMissingVocabWithDictionaryEntries())),
            SpecMenuItem.Command(ShortcutFinger.Home5("Regenerate vocab source answers from jamdict"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.RegenerateJamdictVocabAnswers())),
            SpecMenuItem.Command(ShortcutFinger.Up1("Force flush all cached notes"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.ForceFlushAllNotes())),
            SpecMenuItem.Command(ShortcutFinger.Up2("Force flush all Anki notes by ID"), () => BackgroundTaskManager.Run(FlushAllAnkiNotesById)),
            SpecMenuItem.Command(ShortcutFinger.Up3("Write file system repository"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.WriteFileSystemRepository()))
         }
      );

   SpecMenuItem BuildUpdateSubmenuSpec() =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home1("Update"),
         new List<SpecMenuItem>
         {
            SpecMenuItem.Command(ShortcutFinger.Home1("Vocab"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.UpdateVocab())),
            SpecMenuItem.Command(ShortcutFinger.Home2("Kanji"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.UpdateKanji())),
            SpecMenuItem.Command(ShortcutFinger.Home3("Sentences"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.UpdateSentences())),
            SpecMenuItem.Command(ShortcutFinger.Home4("Tag note metadata"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.TagNoteMetadata())),
            SpecMenuItem.Command(ShortcutFinger.Home5("All the above"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.UpdateAll())),
            SpecMenuItem.Command(ShortcutFinger.Up1("Reparse sentences"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.ReparseAllSentences())),
            SpecMenuItem.Command(ShortcutFinger.Down1("All the above: Full rebuild"), () => BackgroundTaskManager.Run(() => _services.LocalNoteUpdater.FullRebuild()))
         }
      );

   // Config menu actions
   void OnOptions()
   {
      this.Log().Info("OnOptions() called!");
      this.Log().Info("Calling ShowOptionsDialog()...");
      _dialogs.ShowOptionsDialog();
      this.Log().Info("ShowOptionsDialog() completed");
   }

   void OnReadingsMappings() => _dialogs.ShowReadingsMappingsDialog();

   void FlushAllAnkiNotesById()
   {
      using var scope = _services.TaskRunner.Current("Flushing all Anki notes by ID");
      var externalIds = _services.ExternalNoteIdMap.AllExternalIds();
      scope.RunBatch(externalIds, AnkiFacade.Batches.FlushAnkiNote, "Flushing Anki notes");
   }

   // Lookup menu actions
   void OnOpenNote() => _dialogs.ToggleNoteSearchDialog();
}
