using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core.Note;
using System;

namespace JAStudio.UI.ViewModels;

public partial class KanjiEditorViewModel : ObservableObject
{
   readonly KanjiNote _kanji;

#pragma warning disable CS8618
   [Obsolete("Parameterless constructor is only for XAML designer support and should not be used directly.")]
   public KanjiEditorViewModel() {}
#pragma warning restore CS8618

   public KanjiEditorViewModel(KanjiNote kanji)
   {
      _kanji = kanji;
      Title = $"Edit Kanji: {kanji.GetQuestion()}";
      LoadFromNote();
   }

   public string Title { get; }

   // --- Editable fields ---

   [ObservableProperty] string _question = "";
   [ObservableProperty] string _userAnswer = "";
   [ObservableProperty] string _readingOn = "";
   [ObservableProperty] string _readingKun = "";
   [ObservableProperty] string _readingNan = "";
   [ObservableProperty] string _radicals = "";
   [ObservableProperty] string _primaryVocab = "";
   [ObservableProperty] string _userMnemonic = "";
   [ObservableProperty] string _similarMeaning = "";
   [ObservableProperty] string _confusedWith = "";

   // --- Read-only reference fields ---

   [ObservableProperty] string _sourceAnswer = "";
   [ObservableProperty] string _sourceMeaningMnemonic = "";

   // --- Commands ---

   public IRelayCommand SaveCommand { get; set; } = null!;
   public IRelayCommand CancelCommand { get; set; } = null!;

   void LoadFromNote()
   {
      Question = _kanji.GetQuestion();
      UserAnswer = _kanji.UserAnswer;
      ReadingOn = _kanji.ReadingOnHtml;
      ReadingKun = _kanji.ReadingKunHtml;
      ReadingNan = _kanji.ReadingNanHtml;
      Radicals = string.Join(", ", _kanji.Radicals);
      PrimaryVocab = string.Join(", ", _kanji.PrimaryVocab);
      UserMnemonic = _kanji.UserMnemonic;
      SimilarMeaning = string.Join(", ", _kanji.UserSimilarMeaning);
      ConfusedWith = string.Join(", ", _kanji.RelatedConfusedWith);

      SourceAnswer = _kanji.GetField(NoteFieldsConstants.Kanji.SourceAnswer);
      SourceMeaningMnemonic = _kanji.SourceMeaningMnemonic;
   }

   public void Save()
   {
      _kanji.SetQuestion(Question.Trim());
      _kanji.UserAnswer = UserAnswer;
      _kanji.ReadingOnHtml = ReadingOn;
      _kanji.ReadingKunHtml = ReadingKun;
      _kanji.SetField(NoteFieldsConstants.Kanji.ReadingNan, ReadingNan);
      _kanji.SetRadicals(Radicals);
      _kanji.PrimaryVocab = SplitCommaSeparated(PrimaryVocab);
      _kanji.UserMnemonic = UserMnemonic;
      _kanji.SetField(NoteFieldsConstants.Kanji.UserSimilarMeaning, SimilarMeaning);
      _kanji.SetField(NoteFieldsConstants.Kanji.RelatedConfusedWith, ConfusedWith);
      _kanji.SetField(NoteFieldsConstants.Kanji.SourceAnswer, SourceAnswer);
      _kanji.SetField(NoteFieldsConstants.Kanji.SourceMeaningMnemonic, SourceMeaningMnemonic);
      _kanji.UpdateGeneratedData();
   }

   static System.Collections.Generic.List<string> SplitCommaSeparated(string value)
   {
      if(string.IsNullOrWhiteSpace(value)) return [];

      var items = value.Split(',', StringSplitOptions.TrimEntries | StringSplitOptions.RemoveEmptyEntries);
      return [..items];
   }
}
