using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace JAStudio.Core.Configuration;

public static class ConfigurationValue
{
   static Dictionary<string, string>? _configDict;
   static Action<Dictionary<string, string>>? _updateCallback;

   public static void Init(Dictionary<string, string> configDict, Action<Dictionary<string, string>> updateCallback)
   {
      if(_configDict != null)
      {
         throw new InvalidOperationException("Configuration dict already initialized");
      }

      _configDict = configDict;
      _updateCallback = updateCallback;
   }

   internal static Dictionary<string, string> GetConfigDict()
   {
      if(App.IsTesting)
      {
         return new Dictionary<string, string>();
      }

      if(_configDict == null)
      {
         throw new InvalidOperationException("Configuration dict not initialized");
      }

      return _configDict;
   }

   internal static void WriteConfigDict()
   {
      if(!App.IsTesting && _updateCallback != null && _configDict != null)
      {
         _updateCallback(_configDict);
      }
   }

   static JapaneseConfig? _config;

   public static JapaneseConfig Config()
   {
      return _config ??= new JapaneseConfig();
   }
}

public class ConfigurationValue<T>
{
   T _value;
   readonly List<Action<T>> _changeCallbacks = [];

   public string Title { get; }
   public Action<T>? FeatureToggler { get; }
   public string Name { get; }

   public ConfigurationValue(string name, string title, T defaultValue, Func<string, T> converter, Action<T>? featureToggler = null)
   {
      Title = title;
      FeatureToggler = featureToggler;
      Name = name;

      var configDict = ConfigurationValue.GetConfigDict();

      _value = configDict.TryGetValue(name, out var value)
                  ? converter(value)
                  : defaultValue;

      if(FeatureToggler != null)
      {
         App.AddInitHook(ToggleFeature);
      }
   }

   public T GetValue() => _value;

   public void SetValue(T value)
   {
      _value = value;

      ConfigurationValue.GetConfigDict()[Name] = value?.ToString() ?? "";

      ToggleFeature();

      ConfigurationValue.WriteConfigDict();

      foreach(var callback in _changeCallbacks)
      {
         callback(GetValue());
      }
   }

   public void OnChange(Action<T> callback)
   {
      _changeCallbacks.Add(callback);
   }

   public void ToggleFeature()
   {
      FeatureToggler?.Invoke(_value);
   }
}

public class JapaneseConfig
{
   readonly List<Action> _changeCallbacks = [];

   // Configuration value properties
   public ConfigurationValue<float> BoostFailedCardAllowedTimeByFactor { get; }

   public ConfigurationValue<float> AutoadvanceVocabStartingSeconds { get; }
   public ConfigurationValue<float> AutoadvanceVocabHiraganaSeconds { get; }
   public ConfigurationValue<float> AutoadvanceVocabKatakanaSeconds { get; }
   public ConfigurationValue<float> AutoadvanceVocabKanjiSeconds { get; }

   public ConfigurationValue<float> AutoadvanceSentenceStartingSeconds { get; }
   public ConfigurationValue<float> AutoadvanceSentenceHiraganaSeconds { get; }
   public ConfigurationValue<float> AutoadvanceSentenceKatakanaSeconds { get; }
   public ConfigurationValue<float> AutoadvanceSentenceKanjiSeconds { get; }

   public ConfigurationValue<float> MinimumTimeViewingQuestion { get; }
   public ConfigurationValue<float> MinimumTimeViewingAnswer { get; }

   public ConfigurationValue<int> TimeboxVocabRead { get; }
   public ConfigurationValue<int> TimeboxVocabListen { get; }
   public ConfigurationValue<int> TimeboxSentenceRead { get; }
   public ConfigurationValue<int> TimeboxSentenceListen { get; }
   public ConfigurationValue<int> TimeboxKanjiRead { get; }
   public ConfigurationValue<int> DecreaseFailedCardIntervalsInterval { get; }

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
      public static Func<string, int> Int = int.Parse;
      public static Func<string, long> Long = long.Parse;
      public static Func<string, float> Float = float.Parse;
      public static Func<string, bool> Bool = bool.Parse;
   }

   public JapaneseConfig()
   {
      ConfigurationValue<T> Add<T>(ConfigurationValue<T> value)
      {
         value.OnChange(_ => PublishChange());
         return value;
      }
         
      ConfigurationValue<float> AddFloat(ConfigurationValue<float> value) => Add(value);
      ConfigurationValue<int> AddInt(ConfigurationValue<int> value) => Add(value);
      ConfigurationValue<bool> AddBool(ConfigurationValue<bool> value) => Add(value);

      BoostFailedCardAllowedTimeByFactor = AddFloat(new ConfigurationValue<float>("boost_failed_card_allowed_time_by_factor", "Boost Failed Card Allowed Time Factor", 1.5f, To.Float));

      AutoadvanceVocabStartingSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_vocab_starting_seconds", "Starting Seconds", 3.0f, To.Float));
      AutoadvanceVocabHiraganaSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_vocab_hiragana_seconds", "Hiragana Seconds", 0.7f, To.Float));
      AutoadvanceVocabKatakanaSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_vocab_katakana_seconds", "Katakana Seconds", 0.7f, To.Float));
      AutoadvanceVocabKanjiSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_vocab_kanji_seconds", "Kanji Seconds", 1.5f, To.Float));

      AutoadvanceSentenceStartingSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_sentence_starting_seconds", "Starting Seconds", 3.0f, To.Float));
      AutoadvanceSentenceHiraganaSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_sentence_hiragana_seconds", "Hiragana Seconds", 0.7f, To.Float));
      AutoadvanceSentenceKatakanaSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_sentence_katakana_seconds", "Katakana Seconds", 0.7f, To.Float));
      AutoadvanceSentenceKanjiSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_sentence_kanji_seconds", "Kanji Seconds", 1.5f, To.Float));

      MinimumTimeViewingQuestion = AddFloat(new ConfigurationValue<float>("minimum_time_viewing_question", "Minimum time viewing question", 0.5f, To.Float));
      MinimumTimeViewingAnswer = AddFloat(new ConfigurationValue<float>("minimum_time_viewing_answer", "Minimum time viewing answer", 0.5f, To.Float));

      TimeboxVocabRead = AddInt(new ConfigurationValue<int>("time_box_length_vocab_read", "Vocab Read", 15, To.Int));
      TimeboxVocabListen = AddInt(new ConfigurationValue<int>("time_box_length_vocab_listen", "Vocab Listen", 15, To.Int));
      TimeboxSentenceRead = AddInt(new ConfigurationValue<int>("time_box_length_sentence_read", "Sentence Read", 15, To.Int));
      TimeboxSentenceListen = AddInt(new ConfigurationValue<int>("time_box_length_sentence_listen", "Sentence Listen", 15, To.Int));
      TimeboxKanjiRead = AddInt(new ConfigurationValue<int>("time_box_length_kanji", "Kanji", 15, To.Int));
      DecreaseFailedCardIntervalsInterval = AddInt(new ConfigurationValue<int>("decrease_failed_card_intervals_interval", "Failed card again seconds for next again", 60, To.Int));

      // misc toggles
      BoostFailedCardAllowedTime = new ConfigurationValue<bool>("boost_failed_card_allowed_time", "Boost failed card allowed time", true, To.Bool);
      YomitanIntegrationCopyAnswerToClipboard = AddBool(new ConfigurationValue<bool>("yomitan_integration_copy_answer_to_clipboard", "Yomitan integration: Copy reviewer answer to clipboard", false, To.Bool));
      AnkiInternalFsrsSetEnableFsrsShortTermWithSteps = new ConfigurationValue<bool>("fsrs_set_enable_fsrs_short_term_with_steps", "FSRS: Enable short term scheduler with steps", false, To.Bool);
      DecreaseFailedCardIntervals = AddBool(new ConfigurationValue<bool>("decrease_failed_card_intervals", "Decrease failed card intervals", false, To.Bool));
      PreventDoubleClicks = AddBool(new ConfigurationValue<bool>("prevent_double_clicks", "Prevent double clicks", true, To.Bool));
      PreferDefaultMnemonicsToSourceMnemonics = AddBool(new ConfigurationValue<bool>("prefer_default_mnemocs_to_source_mnemonics", "Prefer default mnemonics to source mnemonics", false, To.Bool));

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
      ShowCompoundPartsInSentenceBreakdown = AddBool(new ConfigurationValue<bool>("show_compound_parts_in_sentence_breakdown", "Show compound parts in sentence breakdown", true, To.Bool));
      ShowKanjiInSentenceBreakdown = AddBool(new ConfigurationValue<bool>("show_kanji_in_sentence_breakdown", "Show kanji in sentence breakdown", true, To.Bool));
      ShowKanjiMnemonicsInSentenceBreakdown = AddBool(new ConfigurationValue<bool>("show_kanji_mnemonics_in_sentence_breakdown", "Show kanji mnemonics in sentence breakdown", true, To.Bool));
      ShowSentenceBreakdownInEditMode = AddBool(new ConfigurationValue<bool>("show_sentence_breakdown_in_edit_mode", "Show sentence breakdown in edit mode", false, To.Bool));
      AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound = AddBool(new ConfigurationValue<bool>("automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound", "Automatically yield last token in suru verb compounds to overlapping compounds (Ctrl+Shift+Alt+s)", true, To.Bool));
      AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound = AddBool(new ConfigurationValue<bool>("automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound", "Automatically yield last token in passive verb compounds to overlapping compounds (Ctrl+Shift+Alt+h)", true, To.Bool));
      AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound = AddBool(new ConfigurationValue<bool>("automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound", "Automatically yield last token in causative verb compounds to overlapping compounds (Ctrl+Shift+Alt+t)", true, To.Bool));

      HideCompositionallyTransparentCompounds = AddBool(new ConfigurationValue<bool>("hide_compositionally_transparent_compounds", "Hide compositionally transparent compounds", true, To.Bool));
      HideAllCompounds = AddBool(new ConfigurationValue<bool>("hide_all_compounds", "Hide all compounds", false, To.Bool));

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
      LoadJamdictDbIntoMemory = AddBool(new ConfigurationValue<bool>("load_jamdict_db_into_memory", "Load Jamdict DB into memory [Requires restart]", false, To.Bool));
      PreCacheCardStudyingStatus = AddBool(new ConfigurationValue<bool>("pre_cache_card_studying_status", "Cache card studying status on startup. Only disable for dev/testing purposes. [Requires restart]", false, To.Bool));
      PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses = AddBool(new ConfigurationValue<bool>("prevent_anki_from_garbage_collecting_every_time_a_window_closes", "Prevent Anki from garbage collecting every time a window closes, causing a short hang every time. [Requires restart]", true, To.Bool));
      DisableAllAutomaticGarbageCollection = AddBool(new ConfigurationValue<bool>("disable_periodic_garbage_collection", "Prevent all automatic garbage collection. Will stop the mini-hangs but memory usage will grow gradually. [Requires restart]", false, To.Bool));
      LoadStudioInForeground = AddBool(new ConfigurationValue<bool>("load_studio_in_foreground", "Load Studio in foreground. Makes it clear when done. Anki will be responsive when done. But you can't use anki while loading.", true, To.Bool));

      // memory toggles
      EnableGarbageCollectionDuringBatches = AddBool(new ConfigurationValue<bool>("enable_garbage_collection_during_batches", "Enable Batch GC. [Requires restart]", true, To.Bool));
      EnableAutomaticGarbageCollection = AddBool(new ConfigurationValue<bool>("enable_automatic_garbage_collection", "Enable automatic GC. [Requires restart. Reduces memory usage the most but slows Anki down and may cause crashes due to Qt incompatibility.]", false, To.Bool));
      EnableAutoStringInterning = AddBool(new ConfigurationValue<bool>("enable_auto_string_interning", "Enable automatic string interning. Reduces memory usage at the cost of some CPU overhead and slowdown. [Requires restart]", false, To.Bool));

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
      TrackInstancesInMemory = AddBool(new ConfigurationValue<bool>("track_instances_in_memory", "Track instances in memory. [Requires restart.. Only useful to developers and will use extra memory.]", false, To.Bool));
      EnableTraceMalloc = AddBool(new ConfigurationValue<bool>("enable_trace_malloc", "Enable tracemalloc. Will show memory usage in logs and increase memory usage A LOT. [Requires restart]", false, To.Bool));
      LogWhenFlushingNotes = AddBool(new ConfigurationValue<bool>("log_when_flushing_notes", "Log when flushing notes to backend.", false, To.Bool));

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

      ReadingsMappingsDict = ReadReadingsMappingsFromFile();
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
      var mappingsFilePath = MappingsFilePath();
      File.WriteAllText(mappingsFilePath, mappings);
      ReadingsMappingsDict = ReadReadingsMappingsFromFile();
   }

   public void SetReadingsMappingsForTesting(string mappings)
   {
      ReadingsMappingsDict = ParseMappingsFromString(mappings);
   }

   public static string ReadReadingsMappingsFile() => File.ReadAllText(MappingsFilePath());

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

   static Dictionary<string, string> ReadReadingsMappingsFromFile() => ParseMappingsFromString(ReadReadingsMappingsFile());

   static Dictionary<string, string> ParseMappingsFromString(string mappingsString)
   {
      string ParseValuePart(string valuePart)
      {
         if(valuePart.Contains("<read>"))
         {
            return valuePart;
         }

         if(valuePart.Contains(":"))
         {
            var parts = valuePart.Split([':'], 2);
            return $"<read>{parts[0].Trim()}</read>{parts[1]}";
         }

         return $"<read>{valuePart}</read>";
      }

      return mappingsString.Trim().Split('\n')
                           .Where(line => line.Contains(":"))
                           .Select(line => line.Split([':'], 2))
                           .ToDictionary(
                               parts => parts[0].Trim(),
                               parts => ParseValuePart(parts[1].Trim())
                            );
   }

   static string MappingsFilePath() => Path.Combine(App.UserFilesDir, "readings_mappings.txt");
}
