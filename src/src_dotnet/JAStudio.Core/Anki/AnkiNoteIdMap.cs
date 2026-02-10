using System.Collections.Concurrent;
using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.Anki;

/// <summary>
/// Thread-safe bidirectional mapping between domain NoteIds and Anki long note IDs.
/// Lives in the Anki integration layer — the domain should not reference this directly.
/// </summary>
public class AnkiNoteIdMap
{
   readonly ConcurrentDictionary<NoteId, long> _noteIdToAnki = new();
   readonly ConcurrentDictionary<long, NoteId> _ankiToNoteId = new();

   public void Register(long ankiId, NoteId noteId)
   {
      _ankiToNoteId[ankiId] = noteId;
      _noteIdToAnki[noteId] = ankiId;
   }

   public NoteId? FromAnkiId(long ankiId) => _ankiToNoteId.TryGetValue(ankiId, out var noteId) ? noteId : null;
   public long? ToAnkiId(NoteId noteId) => _noteIdToAnki.TryGetValue(noteId, out var ankiId) ? ankiId : null;

   public long RequireAnkiId(NoteId noteId) => _noteIdToAnki.TryGetValue(noteId, out var ankiId)
      ? ankiId
      : throw new KeyNotFoundException($"No Anki ID mapping found for NoteId {noteId}");

   public void Unregister(long ankiId)
   {
      if(_ankiToNoteId.TryRemove(ankiId, out var noteId))
      {
         _noteIdToAnki.TryRemove(noteId, out _);
      }
   }

   public void Clear()
   {
      _noteIdToAnki.Clear();
      _ankiToNoteId.Clear();
   }
}
