using Avalonia.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using JAStudio.Core.Batches;
using JAStudio.Core.Note;
using JAStudio.UI.Controls;
using MsBox.Avalonia;
using MsBox.Avalonia.Enums;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace JAStudio.UI.ViewModels;

/// <summary>
/// ViewModel for editing VocabNote matching flags, register settings, and string rules.
/// </summary>
public partial class VocabFlagsViewModel : ObservableObject
{
    private readonly VocabNote _vocab;
    private readonly Window? _parentWindow;

    public VocabFlagsViewModel() {}

    public VocabFlagsViewModel(VocabNote vocab, Window? parentWindow = null)
    {
        _vocab = vocab;
        _parentWindow = parentWindow;
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

    // --- Require/Forbid ViewModels ---

    public RequireForbidControlViewModel YieldLastToken { get; private set; } = null!;
    public RequireForbidControlViewModel Surface { get; private set; } = null!;
    public RequireForbidControlViewModel SentenceEnd { get; private set; } = null!;
    public RequireForbidControlViewModel SentenceStart { get; private set; } = null!;
    public RequireForbidControlViewModel SingleToken { get; private set; } = null!;
    public RequireForbidControlViewModel GodanImperative { get; private set; } = null!;
    public RequireForbidControlViewModel GodanImperativePrefix { get; private set; } = null!;
    public RequireForbidControlViewModel GodanPotential { get; private set; } = null!;
    public RequireForbidControlViewModel IchidanImperative { get; private set; } = null!;
    public RequireForbidControlViewModel MasuStem { get; private set; } = null!;
    public RequireForbidControlViewModel Godan { get; private set; } = null!;
    public RequireForbidControlViewModel Ichidan { get; private set; } = null!;
    public RequireForbidControlViewModel Irrealis { get; private set; } = null!;
    public RequireForbidControlViewModel PastTenseStem { get; private set; } = null!;
    public RequireForbidControlViewModel DictionaryFormStem { get; private set; } = null!;
    public RequireForbidControlViewModel DictionaryFormPrefix { get; private set; } = null!;
    public RequireForbidControlViewModel PrecedingAdverb { get; private set; } = null!;
    public RequireForbidControlViewModel TeFormStem { get; private set; } = null!;
    public RequireForbidControlViewModel TeFormPrefix { get; private set; } = null!;

    // --- String Set ViewModels ---

    public StringSetControlViewModel PrefixIsNot { get; private set; } = null!;
    public StringSetControlViewModel RequiredPrefix { get; private set; } = null!;
    public StringSetControlViewModel SuffixIsNot { get; private set; } = null!;
    public StringSetControlViewModel SurfaceIsNot { get; private set; } = null!;
    public StringSetControlViewModel YieldToSurface { get; private set; } = null!;

    // List of all require/forbid controls for change tracking
    private List<RequireForbidControlViewModel> AllRequireForbidControls { get; set; } = new();

    // List of all string set controls for change tracking
    private List<StringSetControlViewModel> AllStringSetControls { get; set; } = new();

    // --- Commands (note: these will be replaced in the code-behind) ---

    public IAsyncRelayCommand SaveCommand { get; set; } = null!;
    public IRelayCommand CancelCommand { get; set; } = null!;

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

        // Require/Forbid controls (Display section)
        YieldLastToken = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.YieldLastToken, "Yield to overlapping following compound", reparseTrigger: false);
        AllRequireForbidControls.Add(YieldLastToken);

        // Require/Forbid controls (Misc matching rules)
        Surface = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.Surface, "Surface");
        SentenceEnd = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.SentenceEnd, "Sentence end");
        SentenceStart = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.SentenceStart, "Sentence start");
        SingleToken = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.SingleToken, "Single token");
        AllRequireForbidControls.AddRange(new[] { Surface, SentenceEnd, SentenceStart, SingleToken });

        // Require/Forbid controls (Stem matching rules)
        GodanImperative = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.GodanImperative, "Godan imperative");
        GodanImperativePrefix = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.GodanImperativePrefix, "Godan imperative prefix");
        GodanPotential = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.GodanPotential, "Godan potential");
        IchidanImperative = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.IchidanImperative, "Ichidan imperative");
        MasuStem = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.MasuStem, "Masu stem");
        Godan = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.Godan, "Godan");
        Ichidan = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.Ichidan, "Ichidan");
        Irrealis = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.Irrealis, "Irrealis");
        PastTenseStem = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.PastTenseStem, "Past tense stem");
        DictionaryFormStem = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.DictionaryFormStem, "Dictionary form stem");
        DictionaryFormPrefix = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.DictionaryFormPrefix, "Dictionary form prefix");
        PrecedingAdverb = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.PrecedingAdverb, "Preceding adverb");
        TeFormStem = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.TeFormStem, "て-form stem");
        TeFormPrefix = new RequireForbidControlViewModel(_vocab.MatchingConfiguration.RequiresForbids.TeFormPrefix, "て-form prefix");
        AllRequireForbidControls.AddRange(new[] { GodanImperative, GodanImperativePrefix, GodanPotential, IchidanImperative, MasuStem, Godan, Ichidan, Irrealis, PastTenseStem, DictionaryFormStem, DictionaryFormPrefix, PrecedingAdverb, TeFormStem, TeFormPrefix });

        // String set controls
        var rules = _vocab.MatchingConfiguration.ConfigurableRules;
        PrefixIsNot = new StringSetControlViewModel(rules.PrefixIsNot, "Prefix is not", _parentWindow);
        RequiredPrefix = new StringSetControlViewModel(rules.RequiredPrefix, "Required prefix", _parentWindow);
        SuffixIsNot = new StringSetControlViewModel(rules.SuffixIsNot, "Suffix is not", _parentWindow);
        SurfaceIsNot = new StringSetControlViewModel(rules.SurfaceIsNot, "Surface is not", _parentWindow);
        YieldToSurface = new StringSetControlViewModel(rules.YieldToSurface, "Yield to surface", _parentWindow);
        AllStringSetControls.AddRange(new[] { PrefixIsNot, RequiredPrefix, SuffixIsNot, SurfaceIsNot, YieldToSurface });
    }

    public async Task SaveAsync()
    {
        SaveToNote();

        // Check if we should prompt to reparse
        if (ShouldPromptToReparse() && _parentWindow != null)
        {
            var messageBox = MessageBoxManager.GetMessageBoxStandard(
                "Reparse Sentences?",
                "You changed settings that affect sentence parsing. Would you like to reparse sentences for this vocab now?",
                ButtonEnum.YesNo,
                Icon.Question);

            var result = await messageBox.ShowWindowDialogAsync(_parentWindow);

            if (result == ButtonResult.Yes)
            {
                // Trigger reparse using C# batch updater
                await Task.Run(() =>
                {
                    LocalNoteUpdater.ReparseSentencesForVocab(_vocab);
                });
            }
        }
        
        // Note: UI refresh is handled by Python layer when dialog closes
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

        // Save string rules
        _vocab.MatchingConfiguration.ConfigurableRules.Save();
        
        // Note: Require/Forbid controls save directly to the note via their fields
    }

    private bool ShouldPromptToReparse()
    {
        // Check if any reparse-triggering flag has changed
        bool changedReparseFlags = AllRequireForbidControls.Any(c => c.RepraiseTrigger && c.HasChanged());
        bool stringRulesModified = AllStringSetControls.Any(c => c.HasChanges());

        return changedReparseFlags || stringRulesModified;
    }
}
