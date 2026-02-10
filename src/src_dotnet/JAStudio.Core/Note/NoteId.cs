using System;

namespace JAStudio.Core.Note;

/// <summary>
/// Base type for domain note identity. Wraps a Guid to provide strong typing.
/// Notes get their identity at construction time and it never changes.
/// </summary>
public abstract record NoteId(Guid Value)
{
   public sealed override string ToString() => Value.ToString();
}

public record VocabId(Guid Value) : NoteId(Value)
{
   public static VocabId New() => new(Guid.NewGuid());
}

public record KanjiId(Guid Value) : NoteId(Value)
{
   public static KanjiId New() => new(Guid.NewGuid());
}

public record SentenceId(Guid Value) : NoteId(Value)
{
   public static SentenceId New() => new(Guid.NewGuid());
}
