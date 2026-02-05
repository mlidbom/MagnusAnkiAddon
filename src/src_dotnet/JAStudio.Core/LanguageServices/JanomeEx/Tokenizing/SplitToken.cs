namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;

// TODO: replace this jack of all trades class with custom classes
public class SplitToken : SplitTokenBase
{
    private readonly bool _isInflectableWord;
    private readonly bool _isNonWordCharacter;
    private readonly bool _isGodanPotentialStem;
    private readonly bool _isGodanImperativeStem;
    private readonly bool _isIchidanImperativeStem;
    private readonly bool _isGodanPotentialInflection;
    private readonly bool _isGodanImperativeInflection;
    private readonly bool _isIchidanImperativeInflection;

    public SplitToken(
        JNToken source,
        string surface,
        string baseForm,
        bool isNonWordCharacter = false,
        bool isInflectableWord = false,
        bool isGodanPotentialStem = false,
        bool isGodanImperativeStem = false,
        bool isIchidanImperativeStem = false,
        bool isGodanPotentialInflection = false,
        bool isGodanImperativeInflection = false,
        bool isIchidanImperativeInflection = false)
        : base(source, surface, baseForm)
    {
        _isInflectableWord = isInflectableWord;
        _isNonWordCharacter = isNonWordCharacter;
        _isGodanPotentialStem = isGodanPotentialStem;
        _isGodanImperativeStem = isGodanImperativeStem;
        _isIchidanImperativeStem = isIchidanImperativeStem;
        _isGodanPotentialInflection = isGodanPotentialInflection;
        _isGodanImperativeInflection = isGodanImperativeInflection;
        _isIchidanImperativeInflection = isIchidanImperativeInflection;
    }

    // <IAnalysisToken implementation>
    public override bool HasTeFormStem => IsGodanPotentialInflection;
    public override bool IsInflectableWord => _isInflectableWord;
    public override bool IsNonWordCharacter => _isNonWordCharacter;
    public override bool IsGodanVerb => IsGodanPotentialStem || IsGodanImperativeStem || IsGodanPotentialInflection || IsGodanImperativeInflection;
    public override bool IsIchidanVerb => IsIchidanImperativeStem || IsIchidanImperativeInflection;
    public override bool IsGodanPotentialStem => _isGodanPotentialStem;
    public override bool IsGodanImperativeStem => _isGodanImperativeStem;
    public override bool IsIchidanImperativeStem => _isIchidanImperativeStem;
    public override bool IsGodanPotentialInflection => _isGodanPotentialInflection;
    public override bool IsGodanImperativeInflection => _isGodanImperativeInflection;
    public override bool IsIchidanImperativeInflection => _isIchidanImperativeInflection;
    // </IAnalysisToken implementation>
}
