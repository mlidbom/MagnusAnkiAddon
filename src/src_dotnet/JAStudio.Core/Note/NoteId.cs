using System;
using System.Security.Cryptography;
using System.Text;

namespace JAStudio.Core.Note;

/// <summary>
/// Base type for domain note identity. Wraps a Guid to provide strong typing.
/// Notes get their identity at construction time and it never changes.
/// </summary>
public record NoteId(Guid Value)
{
   public static readonly NoteId Empty = new(Guid.Empty);
   public bool IsEmpty => Value == Guid.Empty;
   public override string ToString() => Value.ToString();

   /// <summary>
   /// Generates a deterministic Guid from an Anki long note ID.
   /// This provides cross-session stability until the jp_note_id field is persisted in Anki.
   /// Uses SHA256 with a fixed namespace to produce a consistent result.
   /// </summary>
   public static Guid DeterministicGuidFromAnkiId(long ankiId)
   {
      var input = Encoding.UTF8.GetBytes($"JAStudio:AnkiNoteId:{ankiId}");
      var hash = SHA256.HashData(input);
      // Take first 16 bytes of hash as a Guid
      return new Guid(hash.AsSpan(0, 16));
   }
}

public record VocabId(Guid Value) : NoteId(Value)
{
   public new static readonly VocabId Empty = new(Guid.Empty);
   public static VocabId New() => new(Guid.NewGuid());
}

public record KanjiId(Guid Value) : NoteId(Value)
{
   public new static readonly KanjiId Empty = new(Guid.Empty);
   public static KanjiId New() => new(Guid.NewGuid());
}

public record SentenceId(Guid Value) : NoteId(Value)
{
   public new static readonly SentenceId Empty = new(Guid.Empty);
   public static SentenceId New() => new(Guid.NewGuid());
}
