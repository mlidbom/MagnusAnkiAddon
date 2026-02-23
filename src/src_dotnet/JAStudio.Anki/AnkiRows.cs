using LinqToDB.Mapping;
// ReSharper disable UnusedMember.Global
// ReSharper disable ClassNeverInstantiated.Global

namespace JAStudio.Anki;

// @formatter:off

// ── Row types mirroring Anki's SQLite schema ────────────────────────────────
// Property names decode Anki's cryptic abbreviations into readable meanings.
// Column Name= attributes map back to the actual database column names.

// ── notes ───────────────────────────────────────────────────────────────────

[Table(Name = "notes")]
sealed class NoteRow
{
   [PrimaryKey]                                public long   Id             { get; init; } // epoch-ms timestamp (Anki-assigned, not auto-increment)
   [Column(Name = "guid")]                     public string Guid           { get; init; } = ""; // globally unique id (8-char base91)
   [Column(Name = "mid")]                      public long   NoteTypeId     { get; init; } // model (note type) id
   [Column(Name = "mod")]                      public long   ModifiedEpoch  { get; init; } // modification timestamp (epoch seconds)
   [Column(Name = "usn")]                      public long   UpdateSequence { get; init; } // update sequence number for sync
   [Column(Name = "tags")]                     public string Tags           { get; init; } = ""; // space-separated tag list
   [Column(Name = "flds")]                     public string Fields         { get; init; } = ""; // field values joined by \x1f
   [Column(Name = "sfld")]                     public long   SortField      { get; init; } // sort field value (integer for sorting)
   [Column(Name = "csum")]                     public long   Checksum       { get; init; } // field1 checksum for duplicate detection
   [Column(Name = "flags")]                    public long   Flags          { get; init; }
   [Column(Name = "data")]                     public string Data           { get; init; } = ""; // unused, always ""
}

// ── cards ───────────────────────────────────────────────────────────────────

[Table(Name = "cards")]
sealed class CardRow
{
   [PrimaryKey]                                public long   Id                  { get; init; } // epoch-ms timestamp (Anki-assigned, not auto-increment)
   [Column(Name = "nid")]                      public long   NoteId              { get; init; }
   [Column(Name = "did")]                      public long   DeckId              { get; init; }
   [Column(Name = "ord")]                      public int    Ordinal             { get; init; } // which template (0-based)
   [Column(Name = "mod")]                      public long   ModifiedEpoch       { get; init; }
   [Column(Name = "usn")]                      public long   UpdateSequence      { get; init; }
   [Column(Name = "type")]                     public long   CardType            { get; init; } // 0=new, 1=learn, 2=review, 3=relearn
   [Column(Name = "queue")]                    public int    Queue               { get; init; } // -1=suspended, 0=new, 1=learn, 2=review, 3=day-learn, 4=preview
   [Column(Name = "due")]                      public long   Due                 { get; init; } // due date (day number or epoch-seconds depending on type)
   [Column(Name = "ivl")]                      public long   Interval            { get; init; } // current interval in days (negative = seconds)
   [Column(Name = "factor")]                   public long   EaseFactor          { get; init; } // ease factor (per mille: 2500 = 2.5)
   [Column(Name = "reps")]                     public long   ReviewCount         { get; init; }
   [Column(Name = "lapses")]                   public long   LapseCount          { get; init; }
   [Column(Name = "left")]                     public long   RemainingSteps      { get; init; } // learning steps remaining
   [Column(Name = "odue")]                     public long   OriginalDue         { get; init; } // due when in a filtered deck
   [Column(Name = "odid")]                     public long   OriginalDeckId      { get; init; } // original deck id when in a filtered deck
   [Column(Name = "flags")]                    public long   Flags               { get; init; }
   [Column(Name = "data")]                     public string Data                { get; init; } = "";
}

// ── notetypes ───────────────────────────────────────────────────────────────

[Table(Name = "notetypes")]
sealed class NoteTypeRow
{
   [PrimaryKey]                                public long   Id             { get; init; }
   [Column(Name = "name")]                     public string Name           { get; init; } = "";
   [Column(Name = "mtime_secs")]               public long   ModifiedEpoch  { get; init; }
   [Column(Name = "usn")]                      public long   UpdateSequence { get; init; }
   [Column(Name = "config")]                   public byte[] Config         { get; init; } = [];
}

// ── fields ──────────────────────────────────────────────────────────────────

[Table(Name = "fields")]
sealed class FieldRow
{
   [Column(Name = "ntid")]                     public long   NoteTypeId     { get; init; }
   [Column(Name = "ord")]                      public int    Ordinal        { get; init; }
   [Column(Name = "name")]                     public string Name           { get; init; } = "";
   [Column(Name = "config")]                   public byte[] Config         { get; init; } = [];
}

// ── templates ───────────────────────────────────────────────────────────────

[Table(Name = "templates")]
sealed class TemplateRow
{
   [Column(Name = "ntid")]                     public long   NoteTypeId     { get; init; }
   [Column(Name = "ord")]                      public int    Ordinal        { get; init; }
   [Column(Name = "name")]                     public string Name           { get; init; } = "";
   [Column(Name = "mtime_secs")]               public long   ModifiedEpoch  { get; init; }
   [Column(Name = "usn")]                      public long   UpdateSequence { get; init; }
   [Column(Name = "config")]                   public byte[] Config         { get; init; } = [];
}

// ── decks ───────────────────────────────────────────────────────────────────

[Table(Name = "decks")]
sealed class DeckRow
{
   [PrimaryKey]                                public long   Id             { get; init; }
   [Column(Name = "name")]                     public string Name           { get; init; } = "";
   [Column(Name = "mtime_secs")]               public long   ModifiedEpoch  { get; init; }
   [Column(Name = "usn")]                      public long   UpdateSequence { get; init; }
   [Column(Name = "common")]                   public byte[] Common         { get; init; } = [];
   [Column(Name = "kind")]                     public byte[] Kind           { get; init; } = [];
}

// ── deck_config ─────────────────────────────────────────────────────────────

[Table(Name = "deck_config")]
sealed class DeckConfigRow
{
   [PrimaryKey]                                public long   Id             { get; init; }
   [Column(Name = "name")]                     public string Name           { get; init; } = "";
   [Column(Name = "mtime_secs")]               public long   ModifiedEpoch  { get; init; }
   [Column(Name = "usn")]                      public long   UpdateSequence { get; init; }
   [Column(Name = "config")]                   public byte[] Config         { get; init; } = [];
}

// ── config ──────────────────────────────────────────────────────────────────

[Table(Name = "config")]
sealed class ConfigRow
{
   [PrimaryKey, Column(Name = "KEY")]          public string Key            { get; init; } = "";
   [Column(Name = "usn")]                      public long   UpdateSequence { get; init; }
   [Column(Name = "mtime_secs")]               public long   ModifiedEpoch  { get; init; }
   [Column(Name = "val")]                      public byte[] Value          { get; init; } = [];
}

// ── revlog (review log) ─────────────────────────────────────────────────────

[Table(Name = "revlog")]
sealed class ReviewLogRow
{
   [PrimaryKey]                                public long Id               { get; init; } // epoch-ms timestamp (Anki-assigned, not auto-increment)
   [Column(Name = "cid")]                      public long CardId           { get; init; }
   [Column(Name = "usn")]                      public long UpdateSequence   { get; init; }
   [Column(Name = "ease")]                     public long EaseButton       { get; init; } // 1=again, 2=hard, 3=good, 4=easy
   [Column(Name = "ivl")]                      public long IntervalAfter    { get; init; } // interval after review (days, negative = seconds)
   [Column(Name = "lastIvl")]                  public long IntervalBefore   { get; init; } // interval before review
   [Column(Name = "factor")]                   public long EaseFactor       { get; init; } // ease factor after review (per mille)
   [Column(Name = "time")]                     public long DurationMs       { get; init; } // time spent on review in milliseconds
   [Column(Name = "type")]                     public long ReviewType       { get; init; } // 0=learn, 1=review, 2=relearn, 3=filtered, 4=manual
}

// ── graves (deleted items) ──────────────────────────────────────────────────

[Table(Name = "graves")]
sealed class GraveRow
{
   [Column(Name = "oid")]                      public long OriginalId       { get; init; } // id of deleted card/note/deck
   [Column(Name = "type")]                     public long ObjectType       { get; init; } // 0=card, 1=note, 2=deck
   [Column(Name = "usn")]                      public long UpdateSequence   { get; init; }
}

// ── tags ────────────────────────────────────────────────────────────────────

[Table(Name = "tags")]
sealed class TagRow
{
   [PrimaryKey, Column(Name = "tag")]          public string Tag            { get; init; } = "";
   [Column(Name = "usn")]                      public long   UpdateSequence { get; init; }
   [Column(Name = "collapsed")]                public bool   Collapsed      { get; init; }
   [Column(Name = "config")]                   public byte[]? Config        { get; init; }
}

// ── col (collection metadata — legacy, single row) ──────────────────────────

[Table(Name = "col")]
sealed class CollectionRow
{
   [PrimaryKey]                                public long   Id             { get; init; }
   [Column(Name = "crt")]                      public long   CreatedEpoch   { get; init; } // collection creation timestamp
   [Column(Name = "mod")]                      public long   ModifiedEpoch  { get; init; }
   [Column(Name = "scm")]                      public long   SchemaChanged  { get; init; } // schema modification epoch
   [Column(Name = "ver")]                      public long   Version        { get; init; } // schema version
   [Column(Name = "dty")]                      public long   DirtyFlag      { get; init; } // unused since Anki 2.1
   [Column(Name = "usn")]                      public long   UpdateSequence { get; init; }
   [Column(Name = "ls")]                       public long   LastSync       { get; init; }
   [Column(Name = "conf")]                     public string Configuration  { get; init; } = ""; // JSON config
   [Column(Name = "models")]                   public string Models         { get; init; } = ""; // JSON note types (legacy)
   [Column(Name = "decks")]                    public string Decks          { get; init; } = ""; // JSON decks (legacy)
   [Column(Name = "dconf")]                    public string DeckConfigs    { get; init; } = ""; // JSON deck configs (legacy)
   [Column(Name = "tags")]                     public string Tags           { get; init; } = ""; // JSON tags (legacy)
}
