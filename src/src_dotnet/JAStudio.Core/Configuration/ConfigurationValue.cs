using Compze.Utilities.SystemCE;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace JAStudio.Core.Configuration;

public static class ConfigurationValue
{
    private static Dictionary<string, object>? _configDictReal;
    private static Action<Dictionary<string, object>>? _updateCallback;

    public static void Init(Dictionary<string, object> configDict, Action<Dictionary<string, object>> updateCallback)
    {
        if (_configDictReal != null)
        {
            throw new InvalidOperationException("Configuration dict already initialized");
        }

        _configDictReal = configDict;
        _updateCallback = updateCallback;
    }

    private static Dictionary<string, object> GetConfigDict()
    {
        if (App.IsTesting)
        {
            return new Dictionary<string, object>();
        }
        
        if (_configDictReal == null)
        {
            throw new InvalidOperationException("Configuration dict not initialized");
        }
        
        return _configDictReal;
    }

    private static readonly LazyCE<Dictionary<string, object>> _configDict = new(GetConfigDict);

    private static void WriteConfigDict()
    {
        if (!App.IsTesting && _updateCallback != null && _configDictReal != null)
        {
            _updateCallback(_configDictReal);
        }
    }

    private static JapaneseConfig? _config;

    public static JapaneseConfig Config()
    {
        return _config ??= new JapaneseConfig();
    }
}

public class ConfigurationValue<T>
{
    private T _value;
    private readonly List<Action<T>> _changeCallbacks = new();

    public string Title { get; }
    public Action<T>? FeatureToggler { get; }
    public string Name { get; }

    public ConfigurationValue(string name, string title, T defaultValue, Action<T>? featureToggler = null)
    {
        Title = title;
        FeatureToggler = featureToggler;
        Name = name;
        
        var configDict = typeof(ConfigurationValue).GetMethod("GetConfigDict", 
            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static)!
            .Invoke(null, null) as Dictionary<string, object>;
        
        _value = configDict != null && configDict.TryGetValue(name, out var value) && value is T typedValue
            ? typedValue
            : defaultValue;

        if (FeatureToggler != null)
        {
            App.AddInitHook(ToggleFeature);
        }
    }

    public T GetValue()
    {
        return _value;
    }

    public void SetValue(T value)
    {
        _value = value;
        
        var configDict = typeof(ConfigurationValue).GetMethod("GetConfigDict", 
            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static)!
            .Invoke(null, null) as Dictionary<string, object>;
        
        if (configDict != null)
        {
            configDict[Name] = value!;
        }
        
        ToggleFeature();
        
        typeof(ConfigurationValue).GetMethod("WriteConfigDict", 
            System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static)!
            .Invoke(null, null);
        
        foreach (var callback in _changeCallbacks)
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
    private readonly List<Action> _changeCallbacks = new();

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

    public JapaneseConfig()
    {
        ConfigurationValue<float> AddFloat(ConfigurationValue<float> value)
        {
            value.OnChange(_ => PublishChange());
            return value;
        }

        ConfigurationValue<int> AddInt(ConfigurationValue<int> value)
        {
            value.OnChange(_ => PublishChange());
            return value;
        }

        ConfigurationValue<bool> AddBool(ConfigurationValue<bool> value)
        {
            value.OnChange(_ => PublishChange());
            return value;
        }

        BoostFailedCardAllowedTimeByFactor = AddFloat(new ConfigurationValue<float>("boost_failed_card_allowed_time_by_factor", "Boost Failed Card Allowed Time Factor", 1.5f));

        AutoadvanceVocabStartingSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_vocab_starting_seconds", "Starting Seconds", 3.0f));
        AutoadvanceVocabHiraganaSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_vocab_hiragana_seconds", "Hiragana Seconds", 0.7f));
        AutoadvanceVocabKatakanaSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_vocab_katakana_seconds", "Katakana Seconds", 0.7f));
        AutoadvanceVocabKanjiSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_vocab_kanji_seconds", "Kanji Seconds", 1.5f));

        AutoadvanceSentenceStartingSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_sentence_starting_seconds", "Starting Seconds", 3.0f));
        AutoadvanceSentenceHiraganaSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_sentence_hiragana_seconds", "Hiragana Seconds", 0.7f));
        AutoadvanceSentenceKatakanaSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_sentence_katakana_seconds", "Katakana Seconds", 0.7f));
        AutoadvanceSentenceKanjiSeconds = AddFloat(new ConfigurationValue<float>("autoadvance_sentence_kanji_seconds", "Kanji Seconds", 1.5f));

        MinimumTimeViewingQuestion = AddFloat(new ConfigurationValue<float>("minimum_time_viewing_question", "Minimum time viewing question", 0.5f));
        MinimumTimeViewingAnswer = AddFloat(new ConfigurationValue<float>("minimum_time_viewing_answer", "Minimum time viewing answer", 0.5f));

        TimeboxVocabRead = AddInt(new ConfigurationValue<int>("time_box_length_vocab_read", "Vocab Read", 15));
        TimeboxVocabListen = AddInt(new ConfigurationValue<int>("time_box_length_vocab_listen", "Vocab Listen", 15));
        TimeboxSentenceRead = AddInt(new ConfigurationValue<int>("time_box_length_sentence_read", "Sentence Read", 15));
        TimeboxSentenceListen = AddInt(new ConfigurationValue<int>("time_box_length_sentence_listen", "Sentence Listen", 15));
        TimeboxKanjiRead = AddInt(new ConfigurationValue<int>("time_box_length_kanji", "Kanji", 15));
        DecreaseFailedCardIntervalsInterval = AddInt(new ConfigurationValue<int>("decrease_failed_card_intervals_interval", "Failed card again seconds for next again", 60));

        // misc toggles
        BoostFailedCardAllowedTime = new ConfigurationValue<bool>("boost_failed_card_allowed_time", "Boost failed card allowed time", true);
        YomitanIntegrationCopyAnswerToClipboard = AddBool(new ConfigurationValue<bool>("yomitan_integration_copy_answer_to_clipboard", "Yomitan integration: Copy reviewer answer to clipboard", false));
        AnkiInternalFsrsSetEnableFsrsShortTermWithSteps = new ConfigurationValue<bool>("fsrs_set_enable_fsrs_short_term_with_steps", "FSRS: Enable short term scheduler with steps", false);
        DecreaseFailedCardIntervals = AddBool(new ConfigurationValue<bool>("decrease_failed_card_intervals", "Decrease failed card intervals", false));
        PreventDoubleClicks = AddBool(new ConfigurationValue<bool>("prevent_double_clicks", "Prevent double clicks", true));
        PreferDefaultMnemonicsToSourceMnemonics = AddBool(new ConfigurationValue<bool>("prefer_default_mnemocs_to_source_mnemonics", "Prefer default mnemonics to source mnemonics", false));

        MiscToggles = new List<ConfigurationValue<bool>>
        {
            YomitanIntegrationCopyAnswerToClipboard,
            AnkiInternalFsrsSetEnableFsrsShortTermWithSteps,
            DecreaseFailedCardIntervals,
            PreventDoubleClicks,
            BoostFailedCardAllowedTime,
            PreferDefaultMnemonicsToSourceMnemonics
        };

        // sentence_view_toggles
        ShowCompoundPartsInSentenceBreakdown = AddBool(new ConfigurationValue<bool>("show_compound_parts_in_sentence_breakdown", "Show compound parts in sentence breakdown", true));
        ShowKanjiInSentenceBreakdown = AddBool(new ConfigurationValue<bool>("show_kanji_in_sentence_breakdown", "Show kanji in sentence breakdown", true));
        ShowKanjiMnemonicsInSentenceBreakdown = AddBool(new ConfigurationValue<bool>("show_kanji_mnemonics_in_sentence_breakdown", "Show kanji mnemonics in sentence breakdown", true));
        ShowSentenceBreakdownInEditMode = AddBool(new ConfigurationValue<bool>("show_sentence_breakdown_in_edit_mode", "Show sentence breakdown in edit mode", false));
        AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound = AddBool(new ConfigurationValue<bool>("automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound", "Automatically yield last token in suru verb compounds to overlapping compounds (Ctrl+Shift+Alt+s)", true));
        AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound = AddBool(new ConfigurationValue<bool>("automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound", "Automatically yield last token in passive verb compounds to overlapping compounds (Ctrl+Shift+Alt+h)", true));
        AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound = AddBool(new ConfigurationValue<bool>("automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound", "Automatically yield last token in causative verb compounds to overlapping compounds (Ctrl+Shift+Alt+t)", true));

        HideCompositionallyTransparentCompounds = AddBool(new ConfigurationValue<bool>("hide_compositionally_transparent_compounds", "Hide compositionally transparent compounds", true));
        HideAllCompounds = AddBool(new ConfigurationValue<bool>("hide_all_compounds", "Hide all compounds", false));

        SentenceViewToggles = new List<ConfigurationValue<bool>>
        {
            ShowKanjiInSentenceBreakdown,
            ShowCompoundPartsInSentenceBreakdown,
            ShowKanjiMnemonicsInSentenceBreakdown,
            HideCompositionallyTransparentCompounds,
            AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound,
            AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound,
            AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound,
            HideAllCompounds,
            ShowSentenceBreakdownInEditMode
        };

        // performance toggles
        LoadJamdictDbIntoMemory = AddBool(new ConfigurationValue<bool>("load_jamdict_db_into_memory", "Load Jamdict DB into memory [Requires restart]", false));
        PreCacheCardStudyingStatus = AddBool(new ConfigurationValue<bool>("pre_cache_card_studying_status", "Cache card studying status on startup. Only disable for dev/testing purposes. [Requires restart]", false));
        PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses = AddBool(new ConfigurationValue<bool>("prevent_anki_from_garbage_collecting_every_time_a_window_closes", "Prevent Anki from garbage collecting every time a window closes, causing a short hang every time. [Requires restart]", true));
        DisableAllAutomaticGarbageCollection = AddBool(new ConfigurationValue<bool>("disable_periodic_garbage_collection", "Prevent all automatic garbage collection. Will stop the mini-hangs but memory usage will grow gradually. [Requires restart]", false));
        LoadStudioInForeground = AddBool(new ConfigurationValue<bool>("load_studio_in_foreground", "Load Studio in foreground. Makes it clear when done. Anki will be responsive when done. But you can't use anki while loading.", true));

        // memory toggles
        EnableGarbageCollectionDuringBatches = AddBool(new ConfigurationValue<bool>("enable_garbage_collection_during_batches", "Enable Batch GC. [Requires restart]", true));
        EnableAutomaticGarbageCollection = AddBool(new ConfigurationValue<bool>("enable_automatic_garbage_collection", "Enable automatic GC. [Requires restart. Reduces memory usage the most but slows Anki down and may cause crashes due to Qt incompatibility.]", false));
        EnableAutoStringInterning = AddBool(new ConfigurationValue<bool>("enable_auto_string_interning", "Enable automatic string interning. Reduces memory usage at the cost of some CPU overhead and slowdown. [Requires restart]", false));

        PerformanceAndMemoryToggles = new List<ConfigurationValue<bool>>
        {
            LoadStudioInForeground,
            LoadJamdictDbIntoMemory,
            PreCacheCardStudyingStatus,
            PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses,
            DisableAllAutomaticGarbageCollection,
            EnableGarbageCollectionDuringBatches,
            EnableAutomaticGarbageCollection,
            EnableAutoStringInterning
        };

        // developer only toggles
        TrackInstancesInMemory = AddBool(new ConfigurationValue<bool>("track_instances_in_memory", "Track instances in memory. [Requires restart.. Only useful to developers and will use extra memory.]", false));
        EnableTraceMalloc = AddBool(new ConfigurationValue<bool>("enable_trace_malloc", "Enable tracemalloc. Will show memory usage in logs and increase memory usage A LOT. [Requires restart]", false));
        LogWhenFlushingNotes = AddBool(new ConfigurationValue<bool>("log_when_flushing_notes", "Log when flushing notes to backend.", false));
        
        DeveloperOnlyToggles = new List<ConfigurationValue<bool>>
        {
            EnableTraceMalloc,
            TrackInstancesInMemory,
            LogWhenFlushingNotes
        };

        FeatureToggles = new List<(string, List<ConfigurationValue<bool>>)>
        {
            ("Sentence Display", SentenceViewToggles),
            ("Misc", MiscToggles),
            ("Performance and memory usage", PerformanceAndMemoryToggles),
            ("Devolpers only", DeveloperOnlyToggles)
        };

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

    public static string ReadReadingsMappingsFile()
    {
        return File.ReadAllText(MappingsFilePath());
    }

    private void PublishChange()
    {
        foreach (var callback in _changeCallbacks)
        {
            callback();
        }
    }

    public void OnChange(Action callback)
    {
        _changeCallbacks.Add(callback);
    }

    private static Dictionary<string, string> ReadReadingsMappingsFromFile()
    {
        return ParseMappingsFromString(ReadReadingsMappingsFile());
    }

    private static Dictionary<string, string> ParseMappingsFromString(string mappingsString)
    {
        string ParseValuePart(string valuePart)
        {
            if (valuePart.Contains("<read>"))
            {
                return valuePart;
            }
            if (valuePart.Contains(":"))
            {
                var parts = valuePart.Split(new[] { ':' }, 2);
                return $"<read>{parts[0].Trim()}</read>{parts[1]}";
            }
            return $"<read>{valuePart}</read>";
        }

        return mappingsString.Trim().Split('\n')
            .Where(line => line.Contains(":"))
            .Select(line => line.Split(new[] { ':' }, 2))
            .ToDictionary(
                parts => parts[0].Trim(),
                parts => ParseValuePart(parts[1].Trim())
            );
    }

    private static string MappingsFilePath()
    {
        return Path.Combine(App.UserFilesDir, "readings_mappings.txt");
    }
}
