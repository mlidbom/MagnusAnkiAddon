using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core.Note;
using System;

namespace JAStudio.UI.ViewModels;

public partial class VocabEditorViewModel : ObservableObject
{
   readonly VocabNote _vocab;

#pragma warning disable CS8618
   [Obsolete("Parameterless constructor is only for XAML designer support and should not be used directly.")]
   public VocabEditorViewModel() {}
#pragma warning restore CS8618

   public VocabEditorViewModel(VocabNote vocab)
   {
      _vocab = vocab;
      Title = $"Edit Vocab: {vocab.GetQuestion()}";
      LoadFromNote();
   }

   public string Title { get; }

   // --- Editable fields ---

   [ObservableProperty] string _question = "";
   [ObservableProperty] string _readings = "";
   [ObservableProperty] string _forms = "";
   [ObservableProperty] string _userAnswer = "";
   [ObservableProperty] string _userExplanation = "";
   [ObservableProperty] string _userExplanationLong = "";
   [ObservableProperty] string _userMnemonic = "";
   [ObservableProperty] string _partsOfSpeech = "";
   [ObservableProperty] string _userCompounds = "";

   // --- Read-only reference fields ---

   [ObservableProperty] string _sourceAnswer = "";
   [ObservableProperty] string _sourceMnemonic = "";
   [ObservableProperty] string _sourceReadingMnemonic = "";

   // --- Commands ---

   public IRelayCommand SaveCommand { get; set; } = null!;
   public IRelayCommand CancelCommand { get; set; } = null!;

   void LoadFromNote()
   {
      Question = _vocab.Question.DisambiguationName;
      Readings = string.Join(", ", _vocab.GetReadings());
      Forms = string.Join(", ", _vocab.Forms.AllList());
      UserAnswer = _vocab.User.Answer.Value;
      UserExplanation = _vocab.User.Explanation.Value;
      UserExplanationLong = _vocab.User.ExplanationLong.Value;
      UserMnemonic = _vocab.User.Mnemonic.Value;
      PartsOfSpeech = _vocab.PartsOfSpeech.RawStringValue();
      UserCompounds = string.Join(", ", _vocab.CompoundParts.All());

      SourceAnswer = _vocab.SourceAnswer.Value;
      SourceMnemonic = _vocab.GetField(NoteFieldsConstants.Vocab.SourceMnemonic);
      SourceReadingMnemonic = _vocab.GetField(NoteFieldsConstants.Vocab.SourceReadingMnemonic);
   }

   public void Save()
   {
      _vocab.Question.Set(Question.Trim());
      _vocab.SetReadings(SplitCommaSeparated(Readings));
      _vocab.Forms.SetList(SplitCommaSeparated(Forms));
      _vocab.User.Answer.Set(UserAnswer);
      _vocab.User.Explanation.Set(UserExplanation);
      _vocab.User.ExplanationLong.Set(UserExplanationLong);
      _vocab.User.Mnemonic.Set(UserMnemonic);
      _vocab.PartsOfSpeech.SetRawStringValue(PartsOfSpeech);
      _vocab.CompoundParts.Set(SplitCommaSeparated(UserCompounds));
      _vocab.SourceAnswer.Set(SourceAnswer);
      _vocab.SetField(NoteFieldsConstants.Vocab.SourceMnemonic, SourceMnemonic);
      _vocab.SetField(NoteFieldsConstants.Vocab.SourceReadingMnemonic, SourceReadingMnemonic);
      _vocab.UpdateGeneratedData();
   }

   static System.Collections.Generic.List<string> SplitCommaSeparated(string value)
   {
      if(string.IsNullOrWhiteSpace(value)) return [];

      var items = value.Split(',', StringSplitOptions.TrimEntries | StringSplitOptions.RemoveEmptyEntries);
      return [..items];
   }
}
