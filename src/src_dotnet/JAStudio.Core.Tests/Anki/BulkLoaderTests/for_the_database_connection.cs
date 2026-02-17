using System;
using Compze.Utilities.Testing.Must;
using Compze.Utilities.Testing.XUnit.BDD;
using JAStudio.Anki;

// ReSharper disable InconsistentNaming

namespace JAStudio.Core.Tests.Anki.BulkLoaderTests;

public class for_the_database_connection : IDisposable
{
   readonly AnkiDatabase _db = AnkiDatabase.OpenReadOnly(AnkiTestDb.Path);

   public void Dispose() => _db.Dispose();

   public class given_the_test_database : for_the_database_connection
   {
      [XF] public void the_connection_is_not_null() => _db.Connection.Must().NotBeNull();

      [XF] public void the_notetypes_table_has_rows()
      {
         using var cmd = _db.Connection.CreateCommand();
         cmd.CommandText = "SELECT count(*) FROM notetypes";
         ((long)cmd.ExecuteScalar()! > 0).Must().BeTrue();
      }
   }
}
