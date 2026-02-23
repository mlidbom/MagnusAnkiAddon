using LinqToDB.Mapping;

namespace JAStudio.Anki;

[Table(Name = "notetypes")]
sealed class NoteTypeRow
{
   [PrimaryKey] public long Id { get; init; }
   [Column(Name = "name")] public string Name { get; init; } = "";
}

[Table(Name = "fields")]
sealed class FieldRow
{
   [Column(Name = "ntid")] public long NoteTypeId { get; init; }
   [Column(Name = "name")] public string Name { get; init; } = "";
   [Column(Name = "ord")] public int Ordinal { get; init; }
}

[Table(Name = "notes")]
sealed class NoteRow
{
   [PrimaryKey] public long Id { get; init; }
   [Column(Name = "mid")] public long NoteTypeId { get; init; }
   [Column(Name = "tags")] public string Tags { get; init; } = "";
   [Column(Name = "flds")] public string Fields { get; init; } = "";
}

[Table(Name = "cards")]
sealed class CardRow
{
   [PrimaryKey] public long Id { get; init; }
   [Column(Name = "nid")] public long NoteId { get; init; }
   [Column(Name = "ord")] public int Ordinal { get; init; }
   [Column(Name = "queue")] public int Queue { get; init; }
}

[Table(Name = "templates")]
sealed class TemplateRow
{
   [Column(Name = "ntid")] public long NoteTypeId { get; init; }
   [Column(Name = "ord")] public int Ordinal { get; init; }
   [Column(Name = "name")] public string Name { get; init; } = "";
}
