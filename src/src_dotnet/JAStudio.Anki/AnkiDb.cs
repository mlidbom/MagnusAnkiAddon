using System;
using LinqToDB;
using LinqToDB.Data;
using Microsoft.Data.Sqlite;

namespace JAStudio.Anki;

sealed class AnkiDb : DataConnection
{
   AnkiDb(DataOptions options) : base(options) {}

   public ITable<NoteTypeRow> NoteTypes => this.GetTable<NoteTypeRow>();
   public ITable<FieldRow> Fields => this.GetTable<FieldRow>();
   public ITable<NoteRow> Notes => this.GetTable<NoteRow>();
   public ITable<CardRow> Cards => this.GetTable<CardRow>();
   public ITable<TemplateRow> Templates => this.GetTable<TemplateRow>();

   /// <summary>
   /// Open the Anki database for reading as an immutable snapshot.
   /// Uses SQLite URI with immutable=1 to skip all file locking, which avoids
   /// deadlocks between Microsoft.Data.Sqlite's bundled SQLite and Anki's apsw SQLite.
   /// </summary>
   public static AnkiDb OpenReadOnly(string dbFilePath)
   {
      var uri = $"file:{dbFilePath}?immutable=1";
      var connection = new SqliteConnection($"Data Source={uri}");
      connection.Open();

      // Register Anki's custom "unicase" collation (Unicode-aware case-insensitive comparison).
      // Anki registers this via apsw; we approximate it with .NET's OrdinalIgnoreCase.
      connection.CreateCollation("unicase", (x, y) => string.Compare(x, y, StringComparison.OrdinalIgnoreCase));

      return new AnkiDb(new DataOptions().UseSQLite().UseConnection(connection));
   }
}
