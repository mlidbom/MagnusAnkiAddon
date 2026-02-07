namespace JAStudio.Core.Configuration;

public class Settings
{
    readonly TemporaryServiceCollection _services;
    bool _initialized;

    bool _hideTransparentCompounds;
    bool _showBreakdownInEditMode;
    bool _hideAllCompounds;
    bool _logWhenFlushingNotes;
    bool _showCompoundPartsInSentenceBreakdown;
    bool _showKanjiInSentenceBreakdown;
    bool _showKanjiMnemonicsInSentenceBreakdown;
    bool _automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound;
    bool _automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound;
    bool _automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound;

    internal Settings(TemporaryServiceCollection services)
    {
        _services = services;
    }

    void EnsureInitialized()
    {
        if (_initialized) return;
        _initialized = true;
        Refresh();
        TemporaryServiceCollection.Instance.App.Config().OnChange(Refresh);
    }

    void Refresh()
    {
        var config = TemporaryServiceCollection.Instance.App.Config();
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
    }

    public bool HideTransparentCompounds() { EnsureInitialized(); return _hideTransparentCompounds; }
    public bool HideAllCompounds() { EnsureInitialized(); return _hideAllCompounds; }
    public bool ShowBreakdownInEditMode() { EnsureInitialized(); return _showBreakdownInEditMode; }
    public bool LogWhenFlushingNotes() { EnsureInitialized(); return _logWhenFlushingNotes; }
    public bool ShowCompoundPartsInSentenceBreakdown() { EnsureInitialized(); return _showCompoundPartsInSentenceBreakdown; }
    public bool ShowKanjiInSentenceBreakdown() { EnsureInitialized(); return _showKanjiInSentenceBreakdown; }
    public bool ShowKanjiMnemonicsInSentenceBreakdown() { EnsureInitialized(); return _showKanjiMnemonicsInSentenceBreakdown; }
    public bool AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound() { EnsureInitialized(); return _automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound; }
    public bool AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound() { EnsureInitialized(); return _automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound; }
    public bool AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound() { EnsureInitialized(); return _automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound; }
}
