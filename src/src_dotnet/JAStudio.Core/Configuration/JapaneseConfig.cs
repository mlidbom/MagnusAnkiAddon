using System;
using System.Collections.Generic;

namespace JAStudio.Core.Configuration;

public class JapaneseConfig
{
   readonly ConfigurationStore _store;
   readonly List<Action> _changeCallbacks = [];

   // Configuration value properties
   public ConfigurationValue<double> BoostFailedCardAllowedTimeByFactor { get; }

   public ConfigurationValue<double> AutoadvanceVocabStartingSeconds { get; }
   public ConfigurationValue<double> AutoadvanceVocabHiraganaSeconds { get; }
   public ConfigurationValue<double> AutoadvanceVocabKatakanaSeconds { get; }
   public ConfigurationValue<double> AutoadvanceVocabKanjiSeconds { get; }

   public ConfigurationValue<double> AutoadvanceSentenceStartingSeconds { get; }
   public ConfigurationValue<double> AutoadvanceSentenceHiraganaSeconds { get; }
   public ConfigurationValue<double> AutoadvanceSentenceKatakanaSeconds { get; }
   public ConfigurationValue<double> AutoadvanceSentenceKanjiSeconds { get; }

   public ConfigurationValue<double> MinimumTimeViewingQuestion { get; }
   public ConfigurationValue<double> MinimumTimeViewingAnswer { get; }

   public ConfigurationValue<long> TimeboxVocabRead { get; }
   public ConfigurationValue<long> TimeboxVocabListen { get; }
   public ConfigurationValue<long> TimeboxSentenceRead { get; }
   public ConfigurationValue<long> TimeboxSentenceListen { get; }
   public ConfigurationValue<long> TimeboxKanjiRead { get; }
   public ConfigurationValue<long> DecreaseFailedCardIntervalsInterval { get; }

   // Misc toggles
   public ConfigurationValue<bool> BoostFailedCardAllowedTime { get; }
   public ConfigurationValue<bool> YomitanIntegrationCopyAnswerToClipboard { get; }
   public ConfigurationValue<bool> AnkiInternalFsrsSetEnableFsrsShortTermWithSteps { get; }
   public ConfigurationValue<bool> DecreaseFailedCardIntervals { get; }
   public ConfigurationValue<bool> PreventDoubleClicks { get; }
   public ConfigurationValue<bool> PreferDefaultMnemonicsToSourceMnemonics { get; }

   public List<ConfigurationValue<bool>> MiscToggles { get; }

   // Sentence view toggles
   public ConfigurationValue<bool> ShowCompoundPartsInSentenceBreakdown { get; }
   public ConfigurationValue<bool> ShowKanjiInSentenceBreakdown { get; }
   public ConfigurationValue<bool> ShowKanjiMnemonicsInSentenceBreakdown { get; }
   public ConfigurationValue<bool> ShowSentenceBreakdownInEditMode { get; }
   public ConfigurationValue<bool> AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound { get; }
   public ConfigurationValue<bool> AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound { get; }
   public ConfigurationValue<bool> AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound { get; }
   public ConfigurationValue<bool> HideCompositionallyTransparentCompounds { get; }
   public ConfigurationValue<bool> HideAllCompounds { get; }

   public List<ConfigurationValue<bool>> SentenceViewToggles { get; }

   // Performance toggles
   public ConfigurationValue<bool> LoadJamdictDbIntoMemory { get; }
   public ConfigurationValue<bool> PreCacheCardStudyingStatus { get; }
   public ConfigurationValue<bool> PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses { get; }
   public ConfigurationValue<bool> DisableAllAutomaticGarbageCollection { get; }
   public ConfigurationValue<bool> LoadStudioInForeground { get; }

   // Memory toggles
   public ConfigurationValue<bool> EnableGarbageCollectionDuringBatches { get; }
   public ConfigurationValue<bool> EnableAutomaticGarbageCollection { get; }
   public ConfigurationValue<bool> EnableAutoStringInterning { get; }

   public List<ConfigurationValue<bool>> PerformanceAndMemoryToggles { get; }

   // Developer only toggles
   public ConfigurationValue<bool> TrackInstancesInMemory { get; }
   public ConfigurationValue<bool> EnableTraceMalloc { get; }
   public ConfigurationValue<bool> LogWhenFlushingNotes { get; }

   public List<ConfigurationValue<bool>> DeveloperOnlyToggles { get; }

   public List<(string, List<ConfigurationValue<bool>>)> FeatureToggles { get; }

   public Dictionary<string, string> ReadingsMappingsDict { get; private set; }

   static class To
   {
      public static readonly Func<object, long> Long = it => (long)it;
      public static readonly Func<object, double> Double = it => (double)it;
      public static readonly Func<object, bool> Bool = it => (bool)it;
   }

   public JapaneseConfig(ConfigurationStore store)
   {
      _store = store;
      var configDict = _store.GetConfigDict();

      ConfigurationValue<T> New<T>(string name, string title, T defaultValue, Func<object, T> converter)
         => new(name, title, defaultValue, converter, configDict);

      ConfigurationValue<T> Add<T>(ConfigurationValue<T> value)
      {
         value.OnChange(_ =>
         {
            _store.WriteConfigDict();
            PublishChange();
         });
         return value;
      }

      BoostFailedCardAllowedTimeByFactor = Add(New("boost_failed_card_allowed_time_by_factor", "Boost Failed Card Allowed Time Factor", 1.5f, To.Double));

      AutoadvanceVocabStartingSeconds = Add(New("autoadvance_vocab_starting_seconds", "Starting Seconds", 3.0f, To.Double));
      AutoadvanceVocabHiraganaSeconds = Add(New("autoadvance_vocab_hiragana_seconds", "Hiragana Seconds", 0.7f, To.Double));
      AutoadvanceVocabKatakanaSeconds = Add(New("autoadvance_vocab_katakana_seconds", "Katakana Seconds", 0.7f, To.Double));
      AutoadvanceVocabKanjiSeconds = Add(New("autoadvance_vocab_kanji_seconds", "Kanji Seconds", 1.5f, To.Double));

      AutoadvanceSentenceStartingSeconds = Add(New("autoadvance_sentence_starting_seconds", "Starting Seconds", 3.0f, To.Double));
      AutoadvanceSentenceHiraganaSeconds = Add(New("autoadvance_sentence_hiragana_seconds", "Hiragana Seconds", 0.7f, To.Double));
      AutoadvanceSentenceKatakanaSeconds = Add(New("autoadvance_sentence_katakana_seconds", "Katakana Seconds", 0.7f, To.Double));
      AutoadvanceSentenceKanjiSeconds = Add(New("autoadvance_sentence_kanji_seconds", "Kanji Seconds", 1.5f, To.Double));

      MinimumTimeViewingQuestion = Add(New("minimum_time_viewing_question", "Minimum time viewing question", 0.5f, To.Double));
      MinimumTimeViewingAnswer = Add(New("minimum_time_viewing_answer", "Minimum time viewing answer", 0.5f, To.Double));

      TimeboxVocabRead = Add(New("time_box_length_vocab_read", "Vocab Read", 15, To.Long));
      TimeboxVocabListen = Add(New("time_box_length_vocab_listen", "Vocab Listen", 15, To.Long));
      TimeboxSentenceRead = Add(New("time_box_length_sentence_read", "Sentence Read", 15, To.Long));
      TimeboxSentenceListen = Add(New("time_box_length_sentence_listen", "Sentence Listen", 15, To.Long));
      TimeboxKanjiRead = Add(New("time_box_length_kanji", "Kanji", 15, To.Long));
      DecreaseFailedCardIntervalsInterval = Add(New("decrease_failed_card_intervals_interval", "Failed card again seconds for next again", 60, To.Long));

      // misc toggles
      BoostFailedCardAllowedTime = New("boost_failed_card_allowed_time", "Boost failed card allowed time", true, To.Bool);
      YomitanIntegrationCopyAnswerToClipboard = Add(New("yomitan_integration_copy_answer_to_clipboard", "Yomitan integration: Copy reviewer answer to clipboard", false, To.Bool));
      AnkiInternalFsrsSetEnableFsrsShortTermWithSteps = New("fsrs_set_enable_fsrs_short_term_with_steps", "FSRS: Enable short term scheduler with steps", false, To.Bool);
      DecreaseFailedCardIntervals = Add(New("decrease_failed_card_intervals", "Decrease failed card intervals", false, To.Bool));
      PreventDoubleClicks = Add(New("prevent_double_clicks", "Prevent double clicks", true, To.Bool));
      PreferDefaultMnemonicsToSourceMnemonics = Add(New("prefer_default_mnemocs_to_source_mnemonics", "Prefer default mnemonics to source mnemonics", false, To.Bool));

      MiscToggles =
      [
         YomitanIntegrationCopyAnswerToClipboard,
         AnkiInternalFsrsSetEnableFsrsShortTermWithSteps,
         DecreaseFailedCardIntervals,
         PreventDoubleClicks,
         BoostFailedCardAllowedTime,
         PreferDefaultMnemonicsToSourceMnemonics
      ];

      // sentence_view_toggles
      ShowCompoundPartsInSentenceBreakdown = Add(New("show_compound_parts_in_sentence_breakdown", "Show compound parts in sentence breakdown", true, To.Bool));
      ShowKanjiInSentenceBreakdown = Add(New("show_kanji_in_sentence_breakdown", "Show kanji in sentence breakdown", true, To.Bool));
      ShowKanjiMnemonicsInSentenceBreakdown = Add(New("show_kanji_mnemonics_in_sentence_breakdown", "Show kanji mnemonics in sentence breakdown", true, To.Bool));
      ShowSentenceBreakdownInEditMode = Add(New("show_sentence_breakdown_in_edit_mode", "Show sentence breakdown in edit mode", false, To.Bool));
      AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound = Add(New("automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound", "Automatically yield last token in suru verb compounds to overlapping compounds (Ctrl+Shift+Alt+s)", true, To.Bool));
      AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound = Add(New("automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound", "Automatically yield last token in passive verb compounds to overlapping compounds (Ctrl+Shift+Alt+h)", true, To.Bool));
      AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound = Add(New("automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound", "Automatically yield last token in causative verb compounds to overlapping compounds (Ctrl+Shift+Alt+t)", true, To.Bool));

      HideCompositionallyTransparentCompounds = Add(New("hide_compositionally_transparent_compounds", "Hide compositionally transparent compounds", true, To.Bool));
      HideAllCompounds = Add(New("hide_all_compounds", "Hide all compounds", false, To.Bool));

      SentenceViewToggles =
      [
         ShowKanjiInSentenceBreakdown,
         ShowCompoundPartsInSentenceBreakdown,
         ShowKanjiMnemonicsInSentenceBreakdown,
         HideCompositionallyTransparentCompounds,
         AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound,
         AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound,
         AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound,
         HideAllCompounds,
         ShowSentenceBreakdownInEditMode
      ];

      // performance toggles
      LoadJamdictDbIntoMemory = Add(New("load_jamdict_db_into_memory", "Load Jamdict DB into memory [Requires restart]", false, To.Bool));
      PreCacheCardStudyingStatus = Add(New("pre_cache_card_studying_status", "Cache card studying status on startup. Only disable for dev/testing purposes. [Requires restart]", false, To.Bool));
      PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses = Add(New("prevent_anki_from_garbage_collecting_every_time_a_window_closes", "Prevent Anki from garbage collecting every time a window closes, causing a short hang every time. [Requires restart]", true, To.Bool));
      DisableAllAutomaticGarbageCollection = Add(New("disable_periodic_garbage_collection", "Prevent all automatic garbage collection. Will stop the mini-hangs but memory usage will grow gradually. [Requires restart]", false, To.Bool));
      LoadStudioInForeground = Add(New("load_studio_in_foreground", "Load Studio in foreground. Makes it clear when done. Anki will be responsive when done. But you can't use anki while loading.", true, To.Bool));

      // memory toggles
      EnableGarbageCollectionDuringBatches = Add(New("enable_garbage_collection_during_batches", "Enable Batch GC. [Requires restart]", true, To.Bool));
      EnableAutomaticGarbageCollection = Add(New("enable_automatic_garbage_collection", "Enable automatic GC. [Requires restart. Reduces memory usage the most but slows Anki down and may cause crashes due to Qt incompatibility.]", false, To.Bool));
      EnableAutoStringInterning = Add(New("enable_auto_string_interning", "Enable automatic string interning. Reduces memory usage at the cost of some CPU overhead and slowdown. [Requires restart]", false, To.Bool));

      PerformanceAndMemoryToggles =
      [
         LoadStudioInForeground,
         LoadJamdictDbIntoMemory,
         PreCacheCardStudyingStatus,
         PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses,
         DisableAllAutomaticGarbageCollection,
         EnableGarbageCollectionDuringBatches,
         EnableAutomaticGarbageCollection,
         EnableAutoStringInterning
      ];

      // developer only toggles
      TrackInstancesInMemory = Add(New("track_instances_in_memory", "Track instances in memory. [Requires restart.. Only useful to developers and will use extra memory.]", false, To.Bool));
      EnableTraceMalloc = Add(New("enable_trace_malloc", "Enable tracemalloc. Will show memory usage in logs and increase memory usage A LOT. [Requires restart]", false, To.Bool));
      LogWhenFlushingNotes = Add(New("log_when_flushing_notes", "Log when flushing notes to backend.", false, To.Bool));

      DeveloperOnlyToggles =
      [
         EnableTraceMalloc,
         TrackInstancesInMemory,
         LogWhenFlushingNotes
      ];

      FeatureToggles =
      [
         ("Sentence Display", SentenceViewToggles),
         ("Misc", MiscToggles),
         ("Performance and memory usage", PerformanceAndMemoryToggles),
         ("Developers only", DeveloperOnlyToggles)
      ];

      ReadingsMappingsDict = _store.GetReadingsMappings();
   }

   public void ToggleAllSentenceDisplayAutoYieldFlags(bool? value = null)
   {
      var actualValue = value ?? !AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound.GetValue();
      AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound.SetValue(actualValue);
      AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound.SetValue(actualValue);
      AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound.SetValue(actualValue);
   }

   public void SaveMappings(string mappings)
   {
      _store.SaveMappings(mappings);
      ReadingsMappingsDict = _store.GetReadingsMappings();
   }

   public void SetReadingsMappingsForTesting(string mappings)
   {
      _store.SetReadingsMappingsForTesting(mappings);
      ReadingsMappingsDict = _store.GetReadingsMappings();
   }

   public static string ReadReadingsMappingsFile() => TemporaryServiceCollection.Instance.ConfigurationStore.ReadReadingsMappingsFile();

   void PublishChange()
   {
      foreach(var callback in _changeCallbacks)
      {
         callback();
      }
   }

   public void OnChange(Action callback)
   {
      _changeCallbacks.Add(callback);
   }
}
