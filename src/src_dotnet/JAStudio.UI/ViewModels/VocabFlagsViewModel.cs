using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core.Note;

namespace JAStudio.UI.ViewModels;

/// <summary>
/// ViewModel for editing VocabNote matching flags, register settings, and string rules.
/// </summary>
public partial class VocabFlagsViewModel : ObservableObject
{
    private readonly VocabNote _vocab;

    public VocabFlagsViewModel(VocabNote vocab)
    {
        _vocab = vocab;
        Title = $"Edit Flags: {vocab.GetQuestion()}";
        LoadFromNote();
    }

    public string Title { get; }

    // --- Matching Configuration: Bool Flags ---

    [ObservableProperty]
    private bool _isInflectingWord;

    [ObservableProperty]
    private bool _isPoisonWord;

    [ObservableProperty]
    private bool _matchWithPrecedingVowel;

    [ObservableProperty]
    private bool _questionOverridesForm;

    [ObservableProperty]
    private bool _isCompositionallyTransparentCompound;

    // --- Register Flags ---

    [ObservableProperty]
    private bool _archaic;

    [ObservableProperty]
    private bool _childish;

    [ObservableProperty]
    private bool _derogatory;

    [ObservableProperty]
    private bool _formal;

    [ObservableProperty]
    private bool _honorific;

    [ObservableProperty]
    private bool _humble;

    [ObservableProperty]
    private bool _informal;

    [ObservableProperty]
    private bool _literary;

    [ObservableProperty]
    private bool _polite;

    [ObservableProperty]
    private bool _roughMasculine;

    [ObservableProperty]
    private bool _sensitive;

    [ObservableProperty]
    private bool _slang;

    [ObservableProperty]
    private bool _softFeminine;

    [ObservableProperty]
    private bool _vulgar;

    // --- Commands ---

    [RelayCommand]
    private void Save()
    {
        SaveToNote();
        // TODO: Close dialog and optionally trigger reparse
    }

    [RelayCommand]
    private void Cancel()
    {
        // TODO: Close dialog without saving
    }

    // --- Load/Save ---

    private void LoadFromNote()
    {
        // Bool flags
        IsInflectingWord = _vocab.MatchingConfiguration.BoolFlags.IsInflectingWord.IsSet();
        IsPoisonWord = _vocab.MatchingConfiguration.BoolFlags.IsPoisonWord.IsSet();
        MatchWithPrecedingVowel = _vocab.MatchingConfiguration.BoolFlags.MatchWithPrecedingVowel.IsSet();
        QuestionOverridesForm = _vocab.MatchingConfiguration.BoolFlags.QuestionOverridesForm.IsSet();
        IsCompositionallyTransparentCompound = _vocab.MatchingConfiguration.BoolFlags.IsCompositionallyTransparentCompound.IsSet();

        // Register flags
        Archaic = _vocab.Register.Archaic.IsSet();
        Childish = _vocab.Register.Childish.IsSet();
        Derogatory = _vocab.Register.Derogatory.IsSet();
        Formal = _vocab.Register.Formal.IsSet();
        Honorific = _vocab.Register.Honorific.IsSet();
        Humble = _vocab.Register.Humble.IsSet();
        Informal = _vocab.Register.Informal.IsSet();
        Literary = _vocab.Register.Literary.IsSet();
        Polite = _vocab.Register.Polite.IsSet();
        RoughMasculine = _vocab.Register.RoughMasculine.IsSet();
        Sensitive = _vocab.Register.Sensitive.IsSet();
        Slang = _vocab.Register.Slang.IsSet();
        SoftFeminine = _vocab.Register.SoftFeminine.IsSet();
        Vulgar = _vocab.Register.Vulgar.IsSet();
    }

    private void SaveToNote()
    {
        // Bool flags
        _vocab.MatchingConfiguration.BoolFlags.IsInflectingWord.SetTo(IsInflectingWord);
        _vocab.MatchingConfiguration.BoolFlags.IsPoisonWord.SetTo(IsPoisonWord);
        _vocab.MatchingConfiguration.BoolFlags.MatchWithPrecedingVowel.SetTo(MatchWithPrecedingVowel);
        _vocab.MatchingConfiguration.BoolFlags.QuestionOverridesForm.SetTo(QuestionOverridesForm);
        _vocab.MatchingConfiguration.BoolFlags.IsCompositionallyTransparentCompound.SetTo(IsCompositionallyTransparentCompound);

        // Register flags
        _vocab.Register.Archaic.SetTo(Archaic);
        _vocab.Register.Childish.SetTo(Childish);
        _vocab.Register.Derogatory.SetTo(Derogatory);
        _vocab.Register.Formal.SetTo(Formal);
        _vocab.Register.Honorific.SetTo(Honorific);
        _vocab.Register.Humble.SetTo(Humble);
        _vocab.Register.Informal.SetTo(Informal);
        _vocab.Register.Literary.SetTo(Literary);
        _vocab.Register.Polite.SetTo(Polite);
        _vocab.Register.RoughMasculine.SetTo(RoughMasculine);
        _vocab.Register.Sensitive.SetTo(Sensitive);
        _vocab.Register.Slang.SetTo(Slang);
        _vocab.Register.SoftFeminine.SetTo(SoftFeminine);
        _vocab.Register.Vulgar.SetTo(Vulgar);
    }
}
