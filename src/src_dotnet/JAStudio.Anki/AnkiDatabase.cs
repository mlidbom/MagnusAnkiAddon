using System;

namespace JAStudio.Anki;

/// <summary>
/// Provides read-only access to Anki's SQLite collection database from .NET.
/// Opens with immutable=1 to bypass all locking, avoiding conflicts with Anki's own
/// SQLite library (apsw) that holds WAL locks the .NET SQLite cannot coordinate with.
/// </summary>
public sealed class AnkiDatabase : IDisposable
{
   readonly AnkiDb _db;

   AnkiDatabase(AnkiDb db) => _db = db;

   public static AnkiDatabase OpenReadOnly(string dbFilePath) => new(AnkiDb.OpenReadOnly(dbFilePath));

   public Microsoft.Data.Sqlite.SqliteConnection Connection =>
      (Microsoft.Data.Sqlite.SqliteConnection)_db.Connection;

   public void Dispose() => _db.Dispose();
}
