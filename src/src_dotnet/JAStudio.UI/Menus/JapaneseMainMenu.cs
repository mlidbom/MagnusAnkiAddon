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
   readonly Core.TemporaryServiceCollection _services;
   readonly OpenInAnkiMenus _openInAnkiMenus;

   public JapaneseMainMenu(Core.TemporaryServiceCollection services)
   {
      _services = services;
      _openInAnkiMenus = new OpenInAnkiMenus(services);
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

   SpecMenuItem BuildLookupMenuSpec(Func<string> getClipboardContent)
   {
      return SpecMenuItem.Submenu(
         ShortcutFinger.Home2("Lookup"),
         new List<SpecMenuItem>
         {
            SpecMenuItem.Command(ShortcutFinger.Home1("Open note (Ctrl+O)"), OnOpenNote),
            _openInAnkiMenus.BuildOpenInAnkiMenuSpec(getClipboardContent),
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
      JALogger.Log("Calling JAStudioAppRoot.ShowOptionsDialog()...");
      JAStudioAppRoot.ShowOptionsDialog();
      JALogger.Log("JAStudioAppRoot.ShowOptionsDialog() completed");
   }

   void OnReadingsMappings() => JAStudioAppRoot.ShowReadingsMappingsDialog();

   // Lookup menu actions
   void OnOpenNote() => JAStudioAppRoot.ToggleNoteSearchDialog();

   // Local Actions menu actions
   void OnConvertImmersionKitSentences() => AnkiFacade.ConvertImmersionKitSentences();
   void OnCreateMissingVocab() => _services.LocalNoteUpdater.CreateMissingVocabWithDictionaryEntries();
   void OnRegenerateVocabAnswers() => _services.LocalNoteUpdater.RegenerateJamdictVocabAnswers();

   // Update submenu actions
   void OnUpdateVocab() => _services.LocalNoteUpdater.UpdateVocab();
   void OnUpdateKanji() => _services.LocalNoteUpdater.UpdateKanji();
   void OnUpdateSentences() => _services.LocalNoteUpdater.UpdateSentences();
   void OnTagNoteMetadata() => _services.LocalNoteUpdater.TagNoteMetadata();
   void OnUpdateAll() => _services.LocalNoteUpdater.UpdateAll();
   void OnReparseSentences() => _services.LocalNoteUpdater.ReparseAllSentences();
   void OnFullRebuild() => _services.LocalNoteUpdater.FullRebuild();
}
