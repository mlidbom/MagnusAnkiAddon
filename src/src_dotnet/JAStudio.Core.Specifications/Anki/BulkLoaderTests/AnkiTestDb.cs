using System;

namespace JAStudio.Core.Specifications.Anki.BulkLoaderTests;

static class AnkiTestDb
{
   internal static readonly string Path =
      Environment.GetEnvironmentVariable("ANKI_TEST_DB_PATH")
   ?? System.IO.Path.GetFullPath(System.IO.Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "tests", "collection.anki2"));
}
