using JAStudio.Core.Configuration;
using System;

namespace JAStudio.Core.Note;

public class NoteRecursiveFlushGuard
{
    private readonly JPNote _note;
    private int _depth;

    public NoteRecursiveFlushGuard(JPNote note)
    {
        _note = note;
        _depth = 0;
    }

    public IDisposable PauseFlushing()
    {
        if (_depth != 0)
        {
            throw new InvalidOperationException("We don't support nested flushing since the complexities have not been figured out yet");
        }
        
        _depth++;
        return new FlushPauseScope(this);
    }

    private bool ShouldFlush() => _depth == 0;

    public bool IsFlushing => _depth > 0;

    public void Flush()
    {
        if (ShouldFlush())
        {
            using (PauseFlushing())
            {
                if (Settings.LogWhenFlushingNotes())
                {
                    MyLog.Info($"Flushing {_note.GetType().Name}: {_note.GetQuestion()}");
                }
                _note.UpdateInCache();
            }
        }
    }

    private class FlushPauseScope : IDisposable
    {
        private readonly NoteRecursiveFlushGuard _guard;

        public FlushPauseScope(NoteRecursiveFlushGuard guard)
        {
            _guard = guard;
        }

        public void Dispose()
        {
            _guard._depth--;
        }
    }
}
