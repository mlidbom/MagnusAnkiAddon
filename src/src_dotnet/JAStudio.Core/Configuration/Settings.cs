namespace JAStudio.Core.Configuration;

public class Settings
{
    private static Settings? _instance;
    private static bool _initialized;

    private readonly bool _hideTransparentCompounds;
    private readonly bool _showBreakdownInEditMode;
    private readonly bool _hideAllCompounds;
    private readonly bool _logWhenFlushingNotes;
    private readonly bool _showCompoundPartsInSentenceBreakdown;
    private readonly bool _showKanjiInSentenceBreakdown;
    private readonly bool _showKanjiMnemonicsInSentenceBreakdown;
    private readonly bool _automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound;
    private readonly bool _automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound;
    private readonly bool _automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound;

    private Settings()
    {
        var config = App.Config();
        _hideTransparentCompounds = config.HideCompositionallyTransparentCompounds.GetValue();
        _showBreakdownInEditMode = config.ShowSentenceBreakdownInEditMode.GetValue();
        _hideAllCompounds = config.HideAllCompounds.GetValue();
        _logWhenFlushingNotes = config.LogWhenFlushingNotes.GetValue();
        _showCompoundPartsInSentenceBreakdown = config.ShowCompoundPartsInSentenceBreakdown.GetValue();
        _showKanjiInSentenceBreakdown = config.ShowKanjiInSentenceBreakdown.GetValue();
        _showKanjiMnemonicsInSentenceBreakdown = config.ShowKanjiMnemonicsInSentenceBreakdown.GetValue();
        _automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound = config.AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound.GetValue();
        _automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound = config.AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound.GetValue();
        _automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound = config.AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound.GetValue();

        if (!_initialized)
        {
            config.OnChange(ReplaceInstance);
            _initialized = true;
        }
    }

    public static bool HideTransparentCompounds() => GetInstance()._hideTransparentCompounds;
    public static bool HideAllCompounds() => GetInstance()._hideAllCompounds;
    public static bool ShowBreakdownInEditMode() => GetInstance()._showBreakdownInEditMode;
    public static bool LogWhenFlushingNotes() => GetInstance()._logWhenFlushingNotes;
    public static bool ShowCompoundPartsInSentenceBreakdown() => GetInstance()._showCompoundPartsInSentenceBreakdown;
    public static bool ShowKanjiInSentenceBreakdown() => GetInstance()._showKanjiInSentenceBreakdown;
    public static bool ShowKanjiMnemonicsInSentenceBreakdown() => GetInstance()._showKanjiMnemonicsInSentenceBreakdown;
    public static bool AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound() => GetInstance()._automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound;
    public static bool AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound() => GetInstance()._automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound;
    public static bool AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound() => GetInstance()._automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound;

    private static Settings GetInstance()
    {
        return _instance ??= new Settings();
    }

    private static void ReplaceInstance()
    {
        _instance = new Settings();
    }
}
