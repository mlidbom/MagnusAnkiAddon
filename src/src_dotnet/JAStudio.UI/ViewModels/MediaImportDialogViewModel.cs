using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage.Media;
using JAStudio.Core.TaskRunners;

namespace JAStudio.UI.ViewModels;

public partial class MediaImportDialogViewModel : ObservableObject
{
   public static List<string> VocabFieldNames { get; } = Enum.GetNames<VocabMediaField>().ToList();
   public static List<string> SentenceFieldNames { get; } = Enum.GetNames<SentenceMediaField>().ToList();
   public static List<string> KanjiFieldNames { get; } = Enum.GetNames<KanjiMediaField>().ToList();

   readonly TemporaryServiceCollection _services;
   readonly VocabCollection _vocabCollection;
   readonly SentenceCollection _sentenceCollection;
   readonly KanjiCollection _kanjiCollection;
   readonly MediaFileIndex _index;
   readonly MediaStorageService _storageService;
   readonly TaskRunner _taskRunner;

#pragma warning disable CS8618
   [Obsolete("Parameterless constructor is only for XAML designer support and should not be used directly.")]
   public MediaImportDialogViewModel() {}
#pragma warning restore CS8618

   public MediaImportDialogViewModel(TemporaryServiceCollection services)
   {
      _services = services;
      _vocabCollection = services.ServiceLocator.Resolve<VocabCollection>();
      _sentenceCollection = services.ServiceLocator.Resolve<SentenceCollection>();
      _kanjiCollection = services.ServiceLocator.Resolve<KanjiCollection>();
      _index = services.ServiceLocator.Resolve<MediaFileIndex>();
      _storageService = services.ServiceLocator.Resolve<MediaStorageService>();
      _taskRunner = services.TaskRunner;
      LoadPersistedRules();
   }

   // --- Discovery results ---

   public ObservableCollection<UnimportedMediaGroup> VocabGroups { get; } = [];
   public ObservableCollection<UnimportedMediaGroup> SentenceGroups { get; } = [];
   public ObservableCollection<UnimportedMediaGroup> KanjiGroups { get; } = [];

   [ObservableProperty] string _statusText = "Click Scan to discover un-imported media.";
   [ObservableProperty] bool _isScanning;
   [ObservableProperty] bool _hasPlan;

   // --- Current plan ---
   MediaImportPlan? _currentPlan;
   [ObservableProperty] int _filesToImportCount;
   [ObservableProperty] int _alreadyStoredCount;
   [ObservableProperty] int _missingCount;

   // --- Rule editing ---
   public ObservableCollection<EditableImportRule> VocabRules { get; } = [];
   public ObservableCollection<EditableImportRule> SentenceRules { get; } = [];
   public ObservableCollection<EditableImportRule> KanjiRules { get; } = [];

   [RelayCommand]
   void Scan()
   {
      IsScanning = true;
      StatusText = "Scanning notes for un-imported media...";

      BackgroundTaskManager.Run(() =>
      {
         var ankiMediaDir = Core.App.AnkiMediaDir;
         var analyzer = new MediaImportAnalyzer(ankiMediaDir, _index);

         var vocabGroups = ScanNoteType(_vocabCollection.All(), analyzer);
         var sentenceGroups = ScanNoteType(_sentenceCollection.All(), analyzer);
         var kanjiGroups = ScanNoteType(_kanjiCollection.All(), analyzer);

         Avalonia.Threading.Dispatcher.UIThread.Invoke(() =>
         {
            VocabGroups.Clear();
            foreach(var g in vocabGroups) VocabGroups.Add(g);

            SentenceGroups.Clear();
            foreach(var g in sentenceGroups) SentenceGroups.Add(g);

            KanjiGroups.Clear();
            foreach(var g in kanjiGroups) KanjiGroups.Add(g);

            var totalFiles = vocabGroups.Sum(g => g.FileCount) + sentenceGroups.Sum(g => g.FileCount) + kanjiGroups.Sum(g => g.FileCount);
            StatusText = $"Found {totalFiles} un-imported media files across {vocabGroups.Count + sentenceGroups.Count + kanjiGroups.Count} source/field groups.";
            IsScanning = false;
         });
      });
   }

   [RelayCommand]
   void Analyze()
   {
      StatusText = "Analyzing import plan...";
      HasPlan = false;

      BackgroundTaskManager.Run(() =>
      {
         var ankiMediaDir = Core.App.AnkiMediaDir;
         var analyzer = new MediaImportAnalyzer(ankiMediaDir, _index);

         var vocabRules = BuildVocabRules();
         var sentenceRules = BuildSentenceRules();
         var kanjiRules = BuildKanjiRules();

         var vocabPlan = vocabRules.Count > 0 ? analyzer.AnalyzeVocab(_vocabCollection.All(), vocabRules) : new MediaImportPlan();
         var sentencePlan = sentenceRules.Count > 0 ? analyzer.AnalyzeSentences(_sentenceCollection.All(), sentenceRules) : new MediaImportPlan();
         var kanjiPlan = kanjiRules.Count > 0 ? analyzer.AnalyzeKanji(_kanjiCollection.All(), kanjiRules) : new MediaImportPlan();

         var merged = MergePlans(vocabPlan, sentencePlan, kanjiPlan);

         Avalonia.Threading.Dispatcher.UIThread.Invoke(() =>
         {
            _currentPlan = merged;
            FilesToImportCount = merged.FilesToImport.Count;
            AlreadyStoredCount = merged.AlreadyStored.Count;
            MissingCount = merged.Missing.Count;
            HasPlan = true;
            StatusText = $"Plan: {merged.FilesToImport.Count} to import, {merged.AlreadyStored.Count} already stored, {merged.Missing.Count} missing from Anki.";
         });
      });
   }

   [RelayCommand]
   void Import()
   {
      if(_currentPlan == null) return;
      var plan = _currentPlan;
      _currentPlan = null;
      HasPlan = false;
      StatusText = "Importing...";

      BackgroundTaskManager.Run(() =>
      {
         var executor = new MediaImportExecutor(_storageService, _taskRunner);
         executor.Execute(plan);

         Avalonia.Threading.Dispatcher.UIThread.Invoke(() =>
         {
            StatusText = $"Import complete. {plan.FilesToImport.Count} files imported, {plan.AlreadyStored.Count} references updated.";
         });
      });
   }

   [RelayCommand]
   void AddVocabRule() => VocabRules.Add(new EditableImportRule());

   [RelayCommand]
   void AddSentenceRule() => SentenceRules.Add(new EditableImportRule());

   [RelayCommand]
   void AddKanjiRule() => KanjiRules.Add(new EditableImportRule());

   public IRelayCommand? CloseCommand { get; set; }

   void LoadPersistedRules()
   {
      var persisted = MediaImportRulePersistence.Load();
      foreach(var r in persisted.VocabRules)
         VocabRules.Add(new EditableImportRule { SourceTagPrefix = r.Prefix.ToString(), SelectedField = r.Field.ToString(), TargetDirectory = r.TargetDirectory, SelectedCopyright = r.Copyright.ToString() });
      foreach(var r in persisted.SentenceRules)
         SentenceRules.Add(new EditableImportRule { SourceTagPrefix = r.Prefix.ToString(), SelectedField = r.Field.ToString(), TargetDirectory = r.TargetDirectory, SelectedCopyright = r.Copyright.ToString() });
      foreach(var r in persisted.KanjiRules)
         KanjiRules.Add(new EditableImportRule { SourceTagPrefix = r.Prefix.ToString(), SelectedField = r.Field.ToString(), TargetDirectory = r.TargetDirectory, SelectedCopyright = r.Copyright.ToString() });
   }

   [RelayCommand]
   void SaveRules()
   {
      var persisted = new PersistedImportRules
      {
         VocabRules = BuildVocabRules(),
         SentenceRules = BuildSentenceRules(),
         KanjiRules = BuildKanjiRules()
      };
      MediaImportRulePersistence.Save(persisted);
      StatusText = "Rules saved.";
   }

   List<VocabImportRule> BuildVocabRules() =>
      VocabRules.Where(r => r.IsValid)
                .Select(r => new VocabImportRule(
                   SourceTag.Parse(r.SourceTagPrefix),
                   Enum.Parse<VocabMediaField>(r.SelectedField),
                   r.TargetDirectory,
                   Enum.Parse<CopyrightStatus>(r.SelectedCopyright)))
                .ToList();

   List<SentenceImportRule> BuildSentenceRules() =>
      SentenceRules.Where(r => r.IsValid)
                   .Select(r => new SentenceImportRule(
                      SourceTag.Parse(r.SourceTagPrefix),
                      Enum.Parse<SentenceMediaField>(r.SelectedField),
                      r.TargetDirectory,
                      Enum.Parse<CopyrightStatus>(r.SelectedCopyright)))
                   .ToList();

   List<KanjiImportRule> BuildKanjiRules() =>
      KanjiRules.Where(r => r.IsValid)
                .Select(r => new KanjiImportRule(
                   SourceTag.Parse(r.SourceTagPrefix),
                   Enum.Parse<KanjiMediaField>(r.SelectedField),
                   r.TargetDirectory,
                   Enum.Parse<CopyrightStatus>(r.SelectedCopyright)))
                .ToList();

   static MediaImportPlan MergePlans(params MediaImportPlan[] plans)
   {
      var merged = new MediaImportPlan();
      foreach(var plan in plans)
      {
         merged.FilesToImport.AddRange(plan.FilesToImport);
         merged.AlreadyStored.AddRange(plan.AlreadyStored);
         merged.Missing.AddRange(plan.Missing);
      }
      return merged;
   }

   static List<UnimportedMediaGroup> ScanNoteType<TNote>(List<TNote> notes, MediaImportAnalyzer analyzer) where TNote : JPNote
   {
      var groups = new Dictionary<(string SourcePrefix, string FieldName), List<string>>();

      foreach(var note in notes)
      {
         var rawSourceTag = note.GetSourceTag();
         var sourcePrefix = string.IsNullOrEmpty(rawSourceTag) ? "unknown" : rawSourceTag;

         foreach(var mediaRef in GetMediaReferences(note))
         {
            if(analyzer.IsAlreadyStored(mediaRef.FileName)) continue;

            var key = (sourcePrefix, mediaRef.Type == MediaType.Audio ? "Audio" : "Image");
            if(!groups.TryGetValue(key, out var list))
            {
               list = [];
               groups[key] = list;
            }
            list.Add(mediaRef.FileName);
         }
      }

      return groups.Select(kvp => new UnimportedMediaGroup(kvp.Key.SourcePrefix, kvp.Key.FieldName, kvp.Value.Count))
                   .OrderByDescending(g => g.FileCount)
                   .ToList();
   }

   static List<MediaReference> GetMediaReferences(JPNote note) =>
      note switch
      {
         VocabNote v =>
         [
            ..v.Audio.First.GetMediaReferences(),
            ..v.Audio.Second.GetMediaReferences(),
            ..v.Audio.Tts.GetMediaReferences(),
            ..v.Image.GetMediaReferences(),
            ..v.UserImage.GetMediaReferences()
         ],
         SentenceNote s =>
         [
            ..s.Audio.GetMediaReferences(),
            ..s.Screenshot.GetMediaReferences()
         ],
         KanjiNote k =>
         [
            ..k.Audio.GetMediaReferences(),
            ..k.Image.GetMediaReferences()
         ],
         _ => []
      };
}

public record UnimportedMediaGroup(string SourcePrefix, string MediaType, int FileCount);

public partial class EditableImportRule : ObservableObject
{
   [ObservableProperty] string _sourceTagPrefix = "";
   [ObservableProperty] string _selectedField = "";
   [ObservableProperty] string _targetDirectory = "";
   [ObservableProperty] string _selectedCopyright = nameof(CopyrightStatus.Commercial);

   public bool IsValid =>
      !string.IsNullOrWhiteSpace(SourceTagPrefix) &&
      !string.IsNullOrWhiteSpace(SelectedField) &&
      !string.IsNullOrWhiteSpace(TargetDirectory);

   public static List<string> CopyrightOptions { get; } = [nameof(CopyrightStatus.Free), nameof(CopyrightStatus.Commercial)];
}
