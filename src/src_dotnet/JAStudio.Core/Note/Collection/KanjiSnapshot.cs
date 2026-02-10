using System.Linq;

namespace JAStudio.Core.Note.Collection;

public class KanjiSnapshot : CachedNote
{
   public string[] Radicals { get; }
   public string[] Readings { get; }

   public KanjiSnapshot(KanjiNote note) : base(note)
   {
      Radicals = note.GetRadicals().Distinct().ToArray();
      Readings = note.GetReadingsClean().Distinct().ToArray();
   }
}
