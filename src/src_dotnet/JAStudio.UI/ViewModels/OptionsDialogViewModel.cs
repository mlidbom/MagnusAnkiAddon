using Avalonia.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core.Configuration;

namespace JAStudio.UI.ViewModels;

/// <summary>
/// ViewModel for the Japanese Options dialog.
/// Provides two-way bindings to JapaneseConfig values.
/// Changes are automatically saved via ConfigurationValue SetValue().
/// </summary>
public partial class OptionsDialogViewModel : ObservableObject
{
    private readonly Window _window;
    private readonly JapaneseConfig _config;

    public OptionsDialogViewModel(Window window)
    {
        JALogger.Log("OptionsDialogViewModel constructor: starting...");
        _window = window;
        _config = ConfigurationValue.Config();
        JALogger.Log("OptionsDialogViewModel constructor: calling LoadFromConfig()...");
        LoadFromConfig();
        JALogger.Log("OptionsDialogViewModel constructor: completed");
    }

    // --- Numeric Values ---

    [ObservableProperty]
    private double _autoadvanceVocabStartingSeconds;
    partial void OnAutoadvanceVocabStartingSecondsChanged(double value) =>
        _config.AutoadvanceVocabStartingSeconds.SetValue((float)value);

    [ObservableProperty]
    private double _autoadvanceVocabHiraganaSeconds;
    partial void OnAutoadvanceVocabHiraganaSecondsChanged(double value) =>
        _config.AutoadvanceVocabHiraganaSeconds.SetValue((float)value);

    [ObservableProperty]
    private double _autoadvanceVocabKatakanaSeconds;
    partial void OnAutoadvanceVocabKatakanaSecondsChanged(double value) =>
        _config.AutoadvanceVocabKatakanaSeconds.SetValue((float)value);

    [ObservableProperty]
    private double _autoadvanceVocabKanjiSeconds;
    partial void OnAutoadvanceVocabKanjiSecondsChanged(double value) =>
        _config.AutoadvanceVocabKanjiSeconds.SetValue((float)value);

    [ObservableProperty]
    private double _autoadvanceSentenceStartingSeconds;
    partial void OnAutoadvanceSentenceStartingSecondsChanged(double value) =>
        _config.AutoadvanceSentenceStartingSeconds.SetValue((float)value);

    [ObservableProperty]
    private double _autoadvanceSentenceHiraganaSeconds;
    partial void OnAutoadvanceSentenceHiraganaSecondsChanged(double value) =>
        _config.AutoadvanceSentenceHiraganaSeconds.SetValue((float)value);

    [ObservableProperty]
    private double _autoadvanceSentenceKatakanaSeconds;
    partial void OnAutoadvanceSentenceKatakanaSecondsChanged(double value) =>
        _config.AutoadvanceSentenceKatakanaSeconds.SetValue((float)value);

    [ObservableProperty]
    private double _autoadvanceSentenceKanjiSeconds;
    partial void OnAutoadvanceSentenceKanjiSecondsChanged(double value) =>
        _config.AutoadvanceSentenceKanjiSeconds.SetValue((float)value);

    [ObservableProperty]
    private double _boostFailedCardAllowedTimeByFactor;
    partial void OnBoostFailedCardAllowedTimeByFactorChanged(double value) =>
        _config.BoostFailedCardAllowedTimeByFactor.SetValue((float)value);

    [ObservableProperty]
    private long _decreaseFailedCardIntervalsInterval;
    partial void OnDecreaseFailedCardIntervalsIntervalChanged(long value) =>
        _config.DecreaseFailedCardIntervalsInterval.SetValue(value);

    [ObservableProperty]
    private long _timeboxSentenceRead;
    partial void OnTimeboxSentenceReadChanged(long value) =>
        _config.TimeboxSentenceRead.SetValue(value);

    [ObservableProperty]
    private long _timeboxSentenceListen;
    partial void OnTimeboxSentenceListenChanged(long value) =>
        _config.TimeboxSentenceListen.SetValue(value);

    [ObservableProperty]
    private long _timeboxVocabRead;
    partial void OnTimeboxVocabReadChanged(long value) =>
        _config.TimeboxVocabRead.SetValue(value);

    [ObservableProperty]
    private long _timeboxVocabListen;
    partial void OnTimeboxVocabListenChanged(long value) =>
        _config.TimeboxVocabListen.SetValue(value);

    [ObservableProperty]
    private long _timeboxKanjiRead;
    partial void OnTimeboxKanjiReadChanged(long value) =>
        _config.TimeboxKanjiRead.SetValue(value);

    [ObservableProperty]
    private double _minimumTimeViewingQuestion;
    partial void OnMinimumTimeViewingQuestionChanged(double value) =>
        _config.MinimumTimeViewingQuestion.SetValue((float)value);

    [ObservableProperty]
    private double _minimumTimeViewingAnswer;
    partial void OnMinimumTimeViewingAnswerChanged(double value) =>
        _config.MinimumTimeViewingAnswer.SetValue((float)value);

    // --- Sentence Display Toggles ---

    [ObservableProperty]
    private bool _showKanjiInSentenceBreakdown;
    partial void OnShowKanjiInSentenceBreakdownChanged(bool value) =>
        _config.ShowKanjiInSentenceBreakdown.SetValue(value);

    [ObservableProperty]
    private bool _showCompoundPartsInSentenceBreakdown;
    partial void OnShowCompoundPartsInSentenceBreakdownChanged(bool value) =>
        _config.ShowCompoundPartsInSentenceBreakdown.SetValue(value);

    [ObservableProperty]
    private bool _showKanjiMnemonicsInSentenceBreakdown;
    partial void OnShowKanjiMnemonicsInSentenceBreakdownChanged(bool value) =>
        _config.ShowKanjiMnemonicsInSentenceBreakdown.SetValue(value);

    [ObservableProperty]
    private bool _hideCompositionallyTransparentCompounds;
    partial void OnHideCompositionallyTransparentCompoundsChanged(bool value) =>
        _config.HideCompositionallyTransparentCompounds.SetValue(value);

    [ObservableProperty]
    private bool _automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound;
    partial void OnAutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompoundChanged(bool value) =>
        _config.AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound.SetValue(value);

    [ObservableProperty]
    private bool _automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound;
    partial void OnAutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompoundChanged(bool value) =>
        _config.AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound.SetValue(value);

    [ObservableProperty]
    private bool _automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound;
    partial void OnAutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompoundChanged(bool value) =>
        _config.AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound.SetValue(value);

    [ObservableProperty]
    private bool _hideAllCompounds;
    partial void OnHideAllCompoundsChanged(bool value) =>
        _config.HideAllCompounds.SetValue(value);

    [ObservableProperty]
    private bool _showSentenceBreakdownInEditMode;
    partial void OnShowSentenceBreakdownInEditModeChanged(bool value) =>
        _config.ShowSentenceBreakdownInEditMode.SetValue(value);

    // --- Misc Toggles ---

    [ObservableProperty]
    private bool _yomitanIntegrationCopyAnswerToClipboard;
    partial void OnYomitanIntegrationCopyAnswerToClipboardChanged(bool value) =>
        _config.YomitanIntegrationCopyAnswerToClipboard.SetValue(value);

    [ObservableProperty]
    private bool _ankiInternalFsrsSetEnableFsrsShortTermWithSteps;
    partial void OnAnkiInternalFsrsSetEnableFsrsShortTermWithStepsChanged(bool value) =>
        _config.AnkiInternalFsrsSetEnableFsrsShortTermWithSteps.SetValue(value);

    [ObservableProperty]
    private bool _decreaseFailedCardIntervals;
    partial void OnDecreaseFailedCardIntervalsChanged(bool value) =>
        _config.DecreaseFailedCardIntervals.SetValue(value);

    [ObservableProperty]
    private bool _preventDoubleClicks;
    partial void OnPreventDoubleClicksChanged(bool value) =>
        _config.PreventDoubleClicks.SetValue(value);

    [ObservableProperty]
    private bool _boostFailedCardAllowedTime;
    partial void OnBoostFailedCardAllowedTimeChanged(bool value) =>
        _config.BoostFailedCardAllowedTime.SetValue(value);

    [ObservableProperty]
    private bool _preferDefaultMnemonicsToSourceMnemonics;
    partial void OnPreferDefaultMnemonicsToSourceMnemonicsChanged(bool value) =>
        _config.PreferDefaultMnemonicsToSourceMnemonics.SetValue(value);

    // --- Performance and Memory Toggles ---

    [ObservableProperty]
    private bool _loadStudioInForeground;
    partial void OnLoadStudioInForegroundChanged(bool value) =>
        _config.LoadStudioInForeground.SetValue(value);

    [ObservableProperty]
    private bool _loadJamdictDbIntoMemory;
    partial void OnLoadJamdictDbIntoMemoryChanged(bool value) =>
        _config.LoadJamdictDbIntoMemory.SetValue(value);

    [ObservableProperty]
    private bool _preCacheCardStudyingStatus;
    partial void OnPreCacheCardStudyingStatusChanged(bool value) =>
        _config.PreCacheCardStudyingStatus.SetValue(value);

    [ObservableProperty]
    private bool _preventAnkiFromGarbageCollectingEveryTimeAWindowCloses;
    partial void OnPreventAnkiFromGarbageCollectingEveryTimeAWindowClosesChanged(bool value) =>
        _config.PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses.SetValue(value);

    [ObservableProperty]
    private bool _disableAllAutomaticGarbageCollection;
    partial void OnDisableAllAutomaticGarbageCollectionChanged(bool value) =>
        _config.DisableAllAutomaticGarbageCollection.SetValue(value);

    [ObservableProperty]
    private bool _enableGarbageCollectionDuringBatches;
    partial void OnEnableGarbageCollectionDuringBatchesChanged(bool value) =>
        _config.EnableGarbageCollectionDuringBatches.SetValue(value);

    [ObservableProperty]
    private bool _enableAutomaticGarbageCollection;
    partial void OnEnableAutomaticGarbageCollectionChanged(bool value) =>
        _config.EnableAutomaticGarbageCollection.SetValue(value);

    [ObservableProperty]
    private bool _enableAutoStringInterning;
    partial void OnEnableAutoStringInterningChanged(bool value) =>
        _config.EnableAutoStringInterning.SetValue(value);

    // --- Developer Only Toggles ---

    [ObservableProperty]
    private bool _enableTraceMalloc;
    partial void OnEnableTraceMallocChanged(bool value) =>
        _config.EnableTraceMalloc.SetValue(value);

    [ObservableProperty]
    private bool _trackInstancesInMemory;
    partial void OnTrackInstancesInMemoryChanged(bool value) =>
        _config.TrackInstancesInMemory.SetValue(value);

    [ObservableProperty]
    private bool _logWhenFlushingNotes;
    partial void OnLogWhenFlushingNotesChanged(bool value) =>
        _config.LogWhenFlushingNotes.SetValue(value);

    // --- Commands ---

    [RelayCommand]
    private void Close()
    {
        _window.Close();
    }

    // --- Load from Config ---

    private void LoadFromConfig()
    {
        // Numeric values
        AutoadvanceVocabStartingSeconds = _config.AutoadvanceVocabStartingSeconds.GetValue();
        AutoadvanceVocabHiraganaSeconds = _config.AutoadvanceVocabHiraganaSeconds.GetValue();
        AutoadvanceVocabKatakanaSeconds = _config.AutoadvanceVocabKatakanaSeconds.GetValue();
        AutoadvanceVocabKanjiSeconds = _config.AutoadvanceVocabKanjiSeconds.GetValue();

        AutoadvanceSentenceStartingSeconds = _config.AutoadvanceSentenceStartingSeconds.GetValue();
        AutoadvanceSentenceHiraganaSeconds = _config.AutoadvanceSentenceHiraganaSeconds.GetValue();
        AutoadvanceSentenceKatakanaSeconds = _config.AutoadvanceSentenceKatakanaSeconds.GetValue();
        AutoadvanceSentenceKanjiSeconds = _config.AutoadvanceSentenceKanjiSeconds.GetValue();

        BoostFailedCardAllowedTimeByFactor = _config.BoostFailedCardAllowedTimeByFactor.GetValue();
        DecreaseFailedCardIntervalsInterval = _config.DecreaseFailedCardIntervalsInterval.GetValue();

        TimeboxSentenceRead = _config.TimeboxSentenceRead.GetValue();
        TimeboxSentenceListen = _config.TimeboxSentenceListen.GetValue();
        TimeboxVocabRead = _config.TimeboxVocabRead.GetValue();
        TimeboxVocabListen = _config.TimeboxVocabListen.GetValue();
        TimeboxKanjiRead = _config.TimeboxKanjiRead.GetValue();

        MinimumTimeViewingQuestion = _config.MinimumTimeViewingQuestion.GetValue();
        MinimumTimeViewingAnswer = _config.MinimumTimeViewingAnswer.GetValue();

        // Sentence Display
        ShowKanjiInSentenceBreakdown = _config.ShowKanjiInSentenceBreakdown.GetValue();
        ShowCompoundPartsInSentenceBreakdown = _config.ShowCompoundPartsInSentenceBreakdown.GetValue();
        ShowKanjiMnemonicsInSentenceBreakdown = _config.ShowKanjiMnemonicsInSentenceBreakdown.GetValue();
        HideCompositionallyTransparentCompounds = _config.HideCompositionallyTransparentCompounds.GetValue();
        AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound = _config.AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound.GetValue();
        AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound = _config.AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound.GetValue();
        AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound = _config.AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound.GetValue();
        HideAllCompounds = _config.HideAllCompounds.GetValue();
        ShowSentenceBreakdownInEditMode = _config.ShowSentenceBreakdownInEditMode.GetValue();

        // Misc
        YomitanIntegrationCopyAnswerToClipboard = _config.YomitanIntegrationCopyAnswerToClipboard.GetValue();
        AnkiInternalFsrsSetEnableFsrsShortTermWithSteps = _config.AnkiInternalFsrsSetEnableFsrsShortTermWithSteps.GetValue();
        DecreaseFailedCardIntervals = _config.DecreaseFailedCardIntervals.GetValue();
        PreventDoubleClicks = _config.PreventDoubleClicks.GetValue();
        BoostFailedCardAllowedTime = _config.BoostFailedCardAllowedTime.GetValue();
        PreferDefaultMnemonicsToSourceMnemonics = _config.PreferDefaultMnemonicsToSourceMnemonics.GetValue();

        // Performance and Memory
        LoadStudioInForeground = _config.LoadStudioInForeground.GetValue();
        LoadJamdictDbIntoMemory = _config.LoadJamdictDbIntoMemory.GetValue();
        PreCacheCardStudyingStatus = _config.PreCacheCardStudyingStatus.GetValue();
        PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses = _config.PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses.GetValue();
        DisableAllAutomaticGarbageCollection = _config.DisableAllAutomaticGarbageCollection.GetValue();
        EnableGarbageCollectionDuringBatches = _config.EnableGarbageCollectionDuringBatches.GetValue();
        EnableAutomaticGarbageCollection = _config.EnableAutomaticGarbageCollection.GetValue();
        EnableAutoStringInterning = _config.EnableAutoStringInterning.GetValue();

        // Developer Only
        EnableTraceMalloc = _config.EnableTraceMalloc.GetValue();
        TrackInstancesInMemory = _config.TrackInstancesInMemory.GetValue();
        LogWhenFlushingNotes = _config.LogWhenFlushingNotes.GetValue();
    }
}
