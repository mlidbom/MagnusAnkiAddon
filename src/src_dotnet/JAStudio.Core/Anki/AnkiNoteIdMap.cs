using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.Anki;

/// <summary>
/// Bidirectional mapping between domain NoteIds and Anki long note IDs.
/// Lives in the Anki integration layer — the domain should not reference this directly.
/// </summary>
public class AnkiNoteIdMap
{
   readonly Dictionary<NoteId, long> _noteIdToAnki = new();
   readonly Dictionary<long, NoteId> _ankiToNoteId = new();

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
}
