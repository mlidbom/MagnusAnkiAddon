using System;
using Microsoft.Data.Sqlite;

namespace JAStudio.Core.Anki;

/// <summary>
/// Provides read-only access to Anki's SQLite collection database from .NET.
/// Opens the database in read-only mode to safely coexist with the running Anki process.
/// </summary>
public sealed class AnkiDatabase : IDisposable
{
   readonly SqliteConnection _connection;

   AnkiDatabase(SqliteConnection connection) => _connection = connection;

   public static AnkiDatabase OpenReadOnly(string dbFilePath)
   {
      var connectionString = new SqliteConnectionStringBuilder
      {
         DataSource = dbFilePath,
         Mode = SqliteOpenMode.ReadOnly
      }.ToString();

      var connection = new SqliteConnection(connectionString);
      connection.Open();
      return new AnkiDatabase(connection);
   }

   public SqliteConnection Connection => _connection;

   public void Dispose() => _connection.Dispose();
}
