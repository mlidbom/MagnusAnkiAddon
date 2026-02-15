using System;

namespace JAStudio.Core.Note;

public class NoteGuard
{
   readonly Action _flush;

   public NoteGuard(Action flush) => _flush = flush;

   public void Update(Action mutation)
   {
      mutation();
      _flush();
   }

   public void MarkDirty() => _flush();
}
