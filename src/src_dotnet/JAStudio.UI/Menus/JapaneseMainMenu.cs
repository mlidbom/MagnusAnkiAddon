using System;
using System.Collections.Generic;
using JAStudio.UI.Anki;
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

   SpecMenuItem BuildLookupMenuSpec(Func<string> getClipboardContent)
   {
      return SpecMenuItem.Submenu(
         ShortcutFinger.Home2("Lookup"),
         new List<SpecMenuItem>
         {
            SpecMenuItem.Command(ShortcutFinger.Home1("Open note (Ctrl+O)"), OnOpenNote),
            OpenInAnkiMenus.BuildOpenInAnkiMenuSpec(getClipboardContent),
            WebSearchMenus.BuildWebSearchMenuSpec(getClipboardContent)
         }
      );
   }

   SpecMenuItem BuildLocalActionsMenuSpec() =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home3("Local Actions"),
         new List<SpecMenuItem>
         {
            BuildUpdateSubmenuSpec(),
            SpecMenuItem.Command(ShortcutFinger.Home2("Convert Immersion Kit sentences"), OnConvertImmersionKitSentences),
            SpecMenuItem.Command(ShortcutFinger.Home3("Update everything except reparsing sentences"), OnUpdateAll),
            SpecMenuItem.Command(ShortcutFinger.Home4("Create vocab notes for parsed words"), OnCreateMissingVocab),
            SpecMenuItem.Command(ShortcutFinger.Home5("Regenerate vocab source answers from jamdict"), OnRegenerateVocabAnswers)
         }
      );

   SpecMenuItem BuildUpdateSubmenuSpec() =>
      SpecMenuItem.Submenu(
         ShortcutFinger.Home1("Update"),
         new List<SpecMenuItem>
         {
            SpecMenuItem.Command(ShortcutFinger.Home1("Vocab"), OnUpdateVocab),
            SpecMenuItem.Command(ShortcutFinger.Home2("Kanji"), OnUpdateKanji),
            SpecMenuItem.Command(ShortcutFinger.Home3("Sentences"), OnUpdateSentences),
            SpecMenuItem.Command(ShortcutFinger.Home4("Tag note metadata"), OnTagNoteMetadata),
            SpecMenuItem.Command(ShortcutFinger.Home5("All the above"), OnUpdateAll),
            SpecMenuItem.Command(ShortcutFinger.Up1("Reparse sentences"), OnReparseSentences),
            SpecMenuItem.Command(ShortcutFinger.Down1("All the above: Full rebuild"), OnFullRebuild)
         }
      );

   // Config menu actions
   void OnOptions()
   {
      JALogger.Log("OnOptions() called!");
      JALogger.Log("Calling DialogHost.ShowOptionsDialog()...");
      DialogHost.ShowOptionsDialog();
      JALogger.Log("DialogHost.ShowOptionsDialog() completed");
   }

   void OnReadingsMappings() => DialogHost.ShowReadingsMappingsDialog();

   // Lookup menu actions
   void OnOpenNote() => DialogHost.ToggleNoteSearchDialog();

   // Local Actions menu actions
   void OnConvertImmersionKitSentences() => AnkiFacade.ConvertImmersionKitSentences();
   void OnCreateMissingVocab() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.CreateMissingVocabWithDictionaryEntries();
   void OnRegenerateVocabAnswers() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.RegenerateJamdictVocabAnswers();

   // Update submenu actions
   void OnUpdateVocab() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.UpdateVocab();
   void OnUpdateKanji() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.UpdateKanji();
   void OnUpdateSentences() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.UpdateSentences();
   void OnTagNoteMetadata() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.TagNoteMetadata();
   void OnUpdateAll() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.UpdateAll();
   void OnReparseSentences() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.ReparseAllSentences();
   void OnFullRebuild() => Core.TemporaryServiceCollection.Instance.LocalNoteUpdater.FullRebuild();
}
