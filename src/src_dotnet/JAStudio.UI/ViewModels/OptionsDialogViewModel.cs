using Avalonia.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core.Configuration;
using System;
using Compze.Utilities.Logging;

namespace JAStudio.UI.ViewModels;

/// <summary>
/// ViewModel for the Japanese Options dialog.
/// Provides two-way bindings to JapaneseConfig values.
/// Changes are automatically saved via ConfigurationValue SetValue().
/// </summary>
public partial class OptionsDialogViewModel : ObservableObject
{
   readonly Window _window;
   readonly JapaneseConfig _config;
   readonly Core.TemporaryServiceCollection _services;

#pragma warning disable CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider adding the 'required' modifier or declaring as nullable.
   [Obsolete("Parameterless constructor is only for XAML designer support and should not be used directly.")]
   public OptionsDialogViewModel() {}
#pragma warning restore CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider adding the 'required' modifier or declaring as nullable.

   public OptionsDialogViewModel(Window window, Core.TemporaryServiceCollection services)
   {
      this.Log().Info("OptionsDialogViewModel constructor: starting...");
      _window = window;
      _services = services;
      if(Design.IsDesignMode)
      {
         _services.ConfigurationStore.InitForTesting();
      }

      _config = _services.App.Config;
      this.Log().Info("OptionsDialogViewModel constructor: calling LoadFromConfig()...");
      LoadFromConfig();
      this.Log().Info("OptionsDialogViewModel constructor: completed");
   }

   // --- Numeric Values ---

   [ObservableProperty] double _autoadvanceVocabStartingSeconds;

   partial void OnAutoadvanceVocabStartingSecondsChanged(double value) =>
      _config.AutoadvanceVocabStartingSeconds.SetValue((float)value);

   [ObservableProperty] double _autoadvanceVocabHiraganaSeconds;

   partial void OnAutoadvanceVocabHiraganaSecondsChanged(double value) =>
      _config.AutoadvanceVocabHiraganaSeconds.SetValue((float)value);

   [ObservableProperty] double _autoadvanceVocabKatakanaSeconds;

   partial void OnAutoadvanceVocabKatakanaSecondsChanged(double value) =>
      _config.AutoadvanceVocabKatakanaSeconds.SetValue((float)value);

   [ObservableProperty] double _autoadvanceVocabKanjiSeconds;

   partial void OnAutoadvanceVocabKanjiSecondsChanged(double value) =>
      _config.AutoadvanceVocabKanjiSeconds.SetValue((float)value);

   [ObservableProperty] double _autoadvanceSentenceStartingSeconds;

   partial void OnAutoadvanceSentenceStartingSecondsChanged(double value) =>
      _config.AutoadvanceSentenceStartingSeconds.SetValue((float)value);

   [ObservableProperty] double _autoadvanceSentenceHiraganaSeconds;

   partial void OnAutoadvanceSentenceHiraganaSecondsChanged(double value) =>
      _config.AutoadvanceSentenceHiraganaSeconds.SetValue((float)value);

   [ObservableProperty] double _autoadvanceSentenceKatakanaSeconds;

   partial void OnAutoadvanceSentenceKatakanaSecondsChanged(double value) =>
      _config.AutoadvanceSentenceKatakanaSeconds.SetValue((float)value);

   [ObservableProperty] double _autoadvanceSentenceKanjiSeconds;

   partial void OnAutoadvanceSentenceKanjiSecondsChanged(double value) =>
      _config.AutoadvanceSentenceKanjiSeconds.SetValue((float)value);

   [ObservableProperty] double _boostFailedCardAllowedTimeByFactor;

   partial void OnBoostFailedCardAllowedTimeByFactorChanged(double value) =>
      _config.BoostFailedCardAllowedTimeByFactor.SetValue((float)value);

   [ObservableProperty] long _decreaseFailedCardIntervalsInterval;

   partial void OnDecreaseFailedCardIntervalsIntervalChanged(long value) =>
      _config.DecreaseFailedCardIntervalsInterval.SetValue(value);

   [ObservableProperty] long _timeboxSentenceRead;

   partial void OnTimeboxSentenceReadChanged(long value) =>
      _config.TimeboxSentenceRead.SetValue(value);

   [ObservableProperty] long _timeboxSentenceListen;

   partial void OnTimeboxSentenceListenChanged(long value) =>
      _config.TimeboxSentenceListen.SetValue(value);

   [ObservableProperty] long _timeboxVocabRead;

   partial void OnTimeboxVocabReadChanged(long value) =>
      _config.TimeboxVocabRead.SetValue(value);

   [ObservableProperty] long _timeboxVocabListen;

   partial void OnTimeboxVocabListenChanged(long value) =>
      _config.TimeboxVocabListen.SetValue(value);

   [ObservableProperty] long _timeboxKanjiRead;

   partial void OnTimeboxKanjiReadChanged(long value) =>
      _config.TimeboxKanjiRead.SetValue(value);

   [ObservableProperty] double _minimumTimeViewingQuestion;

   partial void OnMinimumTimeViewingQuestionChanged(double value) =>
      _config.MinimumTimeViewingQuestion.SetValue((float)value);

   [ObservableProperty] double _minimumTimeViewingAnswer;

   partial void OnMinimumTimeViewingAnswerChanged(double value) =>
      _config.MinimumTimeViewingAnswer.SetValue((float)value);

   // --- Sentence Display Toggles ---

   [ObservableProperty] bool _showKanjiInSentenceBreakdown;

   partial void OnShowKanjiInSentenceBreakdownChanged(bool value) =>
      _config.ShowKanjiInSentenceBreakdown.SetValue(value);

   [ObservableProperty] bool _showCompoundPartsInSentenceBreakdown;

   partial void OnShowCompoundPartsInSentenceBreakdownChanged(bool value) =>
      _config.ShowCompoundPartsInSentenceBreakdown.SetValue(value);

   [ObservableProperty] bool _showKanjiMnemonicsInSentenceBreakdown;

   partial void OnShowKanjiMnemonicsInSentenceBreakdownChanged(bool value) =>
      _config.ShowKanjiMnemonicsInSentenceBreakdown.SetValue(value);

   [ObservableProperty] bool _hideCompositionallyTransparentCompounds;

   partial void OnHideCompositionallyTransparentCompoundsChanged(bool value) =>
      _config.HideCompositionallyTransparentCompounds.SetValue(value);

   [ObservableProperty] bool _automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound;

   partial void OnAutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompoundChanged(bool value) =>
      _config.AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound.SetValue(value);

   [ObservableProperty] bool _automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound;

   partial void OnAutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompoundChanged(bool value) =>
      _config.AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound.SetValue(value);

   [ObservableProperty] bool _automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound;

   partial void OnAutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompoundChanged(bool value) =>
      _config.AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound.SetValue(value);

   [ObservableProperty] bool _hideAllCompounds;

   partial void OnHideAllCompoundsChanged(bool value) =>
      _config.HideAllCompounds.SetValue(value);

   [ObservableProperty] bool _showSentenceBreakdownInEditMode;

   partial void OnShowSentenceBreakdownInEditModeChanged(bool value) =>
      _config.ShowSentenceBreakdownInEditMode.SetValue(value);

   // --- Misc Toggles ---

   [ObservableProperty] bool _yomitanIntegrationCopyAnswerToClipboard;

   partial void OnYomitanIntegrationCopyAnswerToClipboardChanged(bool value) =>
      _config.YomitanIntegrationCopyAnswerToClipboard.SetValue(value);

   [ObservableProperty] bool _ankiInternalFsrsSetEnableFsrsShortTermWithSteps;

   partial void OnAnkiInternalFsrsSetEnableFsrsShortTermWithStepsChanged(bool value) =>
      _config.AnkiInternalFsrsSetEnableFsrsShortTermWithSteps.SetValue(value);

   [ObservableProperty] bool _decreaseFailedCardIntervals;

   partial void OnDecreaseFailedCardIntervalsChanged(bool value) =>
      _config.DecreaseFailedCardIntervals.SetValue(value);

   [ObservableProperty] bool _preventDoubleClicks;

   partial void OnPreventDoubleClicksChanged(bool value) =>
      _config.PreventDoubleClicks.SetValue(value);

   [ObservableProperty] bool _boostFailedCardAllowedTime;

   partial void OnBoostFailedCardAllowedTimeChanged(bool value) =>
      _config.BoostFailedCardAllowedTime.SetValue(value);

   [ObservableProperty] bool _preferDefaultMnemonicsToSourceMnemonics;

   partial void OnPreferDefaultMnemonicsToSourceMnemonicsChanged(bool value) =>
      _config.PreferDefaultMnemonicsToSourceMnemonics.SetValue(value);

   // --- Performance and Memory Toggles ---

   [ObservableProperty] bool _loadStudioInForeground;

   partial void OnLoadStudioInForegroundChanged(bool value) =>
      _config.LoadStudioInForeground.SetValue(value);

   [ObservableProperty] bool _loadJamdictDbIntoMemory;

   partial void OnLoadJamdictDbIntoMemoryChanged(bool value) =>
      _config.LoadJamdictDbIntoMemory.SetValue(value);

   [ObservableProperty] bool _preCacheCardStudyingStatus;

   partial void OnPreCacheCardStudyingStatusChanged(bool value) =>
      _config.PreCacheCardStudyingStatus.SetValue(value);

   [ObservableProperty] bool _preventAnkiFromGarbageCollectingEveryTimeAWindowCloses;

   partial void OnPreventAnkiFromGarbageCollectingEveryTimeAWindowClosesChanged(bool value) =>
      _config.PreventAnkiFromGarbageCollectingEveryTimeAWindowCloses.SetValue(value);

   [ObservableProperty] bool _disableAllAutomaticGarbageCollection;

   partial void OnDisableAllAutomaticGarbageCollectionChanged(bool value) =>
      _config.DisableAllAutomaticGarbageCollection.SetValue(value);

   [ObservableProperty] bool _enableGarbageCollectionDuringBatches;

   partial void OnEnableGarbageCollectionDuringBatchesChanged(bool value) =>
      _config.EnableGarbageCollectionDuringBatches.SetValue(value);

   [ObservableProperty] bool _enableAutomaticGarbageCollection;

   partial void OnEnableAutomaticGarbageCollectionChanged(bool value) =>
      _config.EnableAutomaticGarbageCollection.SetValue(value);

   [ObservableProperty] long _reanalysisThreads;

   partial void OnReanalysisThreadsChanged(long value) =>
      _config.ReanalysisThreads.SetValue(value);

   // --- Developer Only Toggles ---

   [ObservableProperty] bool _enableTraceMalloc;

   partial void OnEnableTraceMallocChanged(bool value) =>
      _config.EnableTraceMalloc.SetValue(value);

   [ObservableProperty] bool _trackInstancesInMemory;

   partial void OnTrackInstancesInMemoryChanged(bool value) =>
      _config.TrackInstancesInMemory.SetValue(value);

   [ObservableProperty] bool _logWhenFlushingNotes;

   partial void OnLogWhenFlushingNotesChanged(bool value) =>
      _config.LogWhenFlushingNotes.SetValue(value);

   [ObservableProperty] bool _loadNotesFromFileSystem;

   partial void OnLoadNotesFromFileSystemChanged(bool value) =>
      _config.LoadNotesFromFileSystem.SetValue(value);

   // --- Commands ---

   [RelayCommand] void Close()
   {
      _window.Close();
   }

   // --- Load from Config ---

   void LoadFromConfig()
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
      ReanalysisThreads = _config.ReanalysisThreads.GetValue();

      // Developer Only
      EnableTraceMalloc = _config.EnableTraceMalloc.GetValue();
      TrackInstancesInMemory = _config.TrackInstancesInMemory.GetValue();
      LogWhenFlushingNotes = _config.LogWhenFlushingNotes.GetValue();
      LoadNotesFromFileSystem = _config.LoadNotesFromFileSystem.GetValue();
   }
}
