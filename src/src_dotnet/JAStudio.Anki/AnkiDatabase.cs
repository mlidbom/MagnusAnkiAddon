using System;
using Microsoft.Data.Sqlite;

namespace JAStudio.Anki;

/// <summary>
/// Provides read-only access to Anki's SQLite collection database from .NET.
/// Opens with immutable=1 to bypass all locking, avoiding conflicts with Anki's own
/// SQLite library (apsw) that holds WAL locks the .NET SQLite cannot coordinate with.
/// </summary>
public sealed class AnkiDatabase : IDisposable
{
   AnkiDatabase(SqliteConnection connection) => Connection = connection;

   /// <summary>
   /// Open the Anki database for reading as an immutable snapshot.
   /// Uses SQLite URI with immutable=1 to skip all file locking, which avoids
   /// deadlocks between Microsoft.Data.Sqlite's bundled SQLite and Anki's apsw SQLite.
   /// </summary>
   public static AnkiDatabase OpenReadOnly(string dbFilePath)
   {
      // SQLite URI format with immutable=1: no locks acquired, reads the file as-is.
      var uri = $"file:{dbFilePath}?immutable=1";

      // Use a raw connection string with URI to enable the immutable parameter.
      // SqliteConnectionStringBuilder may not pass URI parameters correctly.
      var connectionString = $"Data Source={uri}";

      var connection = new SqliteConnection(connectionString);
      connection.Open();

      // Register Anki's custom "unicase" collation (Unicode-aware case-insensitive comparison).
      // Anki registers this via apsw; we approximate it with .NET's OrdinalIgnoreCase.
      connection.CreateCollation("unicase", (x, y) => string.Compare(x, y, StringComparison.OrdinalIgnoreCase));

      return new AnkiDatabase(connection);
   }

   public SqliteConnection Connection { get; }

   public void Dispose() => Connection.Dispose();
}
