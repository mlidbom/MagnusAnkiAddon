namespace JAStudio.Core.Configuration;

public class Settings
{
   readonly JapaneseConfig _config;
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

   internal Settings(JapaneseConfig config) => _config = config;

   void EnsureInitialized()
   {
      if(_initialized) return;
      _initialized = true;
      Refresh();
      _config.OnChange(Refresh);
   }

   void Refresh()
   {
      var config = _config;
      _hideTransparentCompounds = config.HideCompositionallyTransparentCompounds.Value;
      _showBreakdownInEditMode = config.ShowSentenceBreakdownInEditMode.Value;
      _hideAllCompounds = config.HideAllCompounds.Value;
      _logWhenFlushingNotes = config.LogWhenFlushingNotes.Value;
      _showCompoundPartsInSentenceBreakdown = config.ShowCompoundPartsInSentenceBreakdown.Value;
      _showKanjiInSentenceBreakdown = config.ShowKanjiInSentenceBreakdown.Value;
      _showKanjiMnemonicsInSentenceBreakdown = config.ShowKanjiMnemonicsInSentenceBreakdown.Value;
      _automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound = config.AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound.Value;
      _automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound = config.AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound.Value;
      _automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound = config.AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound.Value;
   }

   public bool HideTransparentCompounds()
   {
      EnsureInitialized();
      return _hideTransparentCompounds;
   }

   public bool HideAllCompounds()
   {
      EnsureInitialized();
      return _hideAllCompounds;
   }

   public bool ShowBreakdownInEditMode()
   {
      EnsureInitialized();
      return _showBreakdownInEditMode;
   }

   public bool LogWhenFlushingNotes()
   {
      EnsureInitialized();
      return _logWhenFlushingNotes;
   }

   public bool ShowCompoundPartsInSentenceBreakdown()
   {
      EnsureInitialized();
      return _showCompoundPartsInSentenceBreakdown;
   }

   public bool ShowKanjiInSentenceBreakdown()
   {
      EnsureInitialized();
      return _showKanjiInSentenceBreakdown;
   }

   public bool ShowKanjiMnemonicsInSentenceBreakdown()
   {
      EnsureInitialized();
      return _showKanjiMnemonicsInSentenceBreakdown;
   }

   public bool AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound()
   {
      EnsureInitialized();
      return _automaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound;
   }

   public bool AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound()
   {
      EnsureInitialized();
      return _automaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound;
   }

   public bool AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound()
   {
      EnsureInitialized();
      return _automaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound;
   }
}
