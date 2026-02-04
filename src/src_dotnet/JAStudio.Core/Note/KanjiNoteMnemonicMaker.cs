using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.Note;

public static class KanjiNoteMnemonicMaker
{
    public static string CreateDefaultMnemonic(KanjiNote kanjiNote)
    {
        // Stub implementation - this is a complex feature
        // that requires reading mappings configuration
        
        var onReadings = kanjiNote.GetReadingsOn();
        var kunReadings = kanjiNote.GetReadingsKun();
        
        var allReadings = new List<string>();
        allReadings.AddRange(onReadings);
        allReadings.AddRange(kunReadings);
        
        if (!allReadings.Any())
            return string.Empty;
        
        // For now, just return a simple romanized version
        var romanized = string.Join(", ", allReadings.Select(r => KanaUtils.Romanize(r)));
        return $"Reading: {romanized}";
    }
}
