using System;
using System.IO;
using System.Linq;
using JAStudio.Anki;
using JAStudio.Core.Note;
using Xunit;

namespace JAStudio.Core.Tests.Anki;

public class BulkLoaderTests
{
   static readonly string TestDbPath =
      Environment.GetEnvironmentVariable("ANKI_TEST_DB_PATH")
      ?? Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "tests", "collection.anki2"));

   // ── AnkiDatabase ──

   [Fact]
   public void OpenReadOnly_succeeds_on_test_database()
   {
      using var db = AnkiDatabase.OpenReadOnly(TestDbPath);
      Assert.NotNull(db.Connection);
   }

   [Fact]
   public void Can_query_notetypes_table()
   {
      using var db = AnkiDatabase.OpenReadOnly(TestDbPath);
      using var cmd = db.Connection.CreateCommand();
      cmd.CommandText = "SELECT count(*) FROM notetypes";
      var count = (long)cmd.ExecuteScalar()!;
      Assert.True(count > 0, $"Expected notetypes, got {count}");
   }

   // ── NoteBulkLoader ──

   [Fact]
   public void LoadAllNotesOfType_loads_vocab_notes()
   {
      var result = NoteBulkLoader.LoadAllNotesOfType(TestDbPath, NoteTypes.Vocab, g => new VocabId(g));
      Assert.NotEmpty(result.Notes);
      Assert.All(result.Notes, n =>
      {
         Assert.NotNull(n.Id);
         Assert.NotEmpty(n.Fields);
      });
   }

   [Fact]
   public void LoadAllNotesOfType_loads_kanji_notes()
   {
      var result = NoteBulkLoader.LoadAllNotesOfType(TestDbPath, NoteTypes.Kanji, g => new KanjiId(g));
      Assert.NotEmpty(result.Notes);
      Assert.All(result.Notes, n => Assert.NotNull(n.Id));
   }

   [Fact]
   public void LoadAllNotesOfType_loads_sentence_notes()
   {
      var result = NoteBulkLoader.LoadAllNotesOfType(TestDbPath, NoteTypes.Sentence, g => new SentenceId(g));
      Assert.NotEmpty(result.Notes);
      Assert.All(result.Notes, n => Assert.NotNull(n.Id));
   }

   [Fact]
   public void LoadAllNotesOfType_throws_for_unknown_note_type()
   {
      Assert.Throws<System.Collections.Generic.KeyNotFoundException>(
         () => NoteBulkLoader.LoadAllNotesOfType(TestDbPath, "NonExistentNoteType", g => new VocabId(g)));
   }

   [Fact]
   public void LoadAllNotesOfType_vocab_notes_have_expected_fields()
   {
      var result = NoteBulkLoader.LoadAllNotesOfType(TestDbPath, NoteTypes.Vocab, g => new VocabId(g));
      var first = result.Notes.First();
      Assert.True(first.Fields.ContainsKey("Q"), $"Fields: [{string.Join(", ", first.Fields.Keys)}]");
      Assert.True(first.Fields.ContainsKey("A"));
      Assert.True(first.Fields.ContainsKey("Reading"));
   }

   [Fact]
   public void LoadAllNotesOfType_kanji_notes_have_expected_fields()
   {
      var result = NoteBulkLoader.LoadAllNotesOfType(TestDbPath, NoteTypes.Kanji, g => new KanjiId(g));
      var first = result.Notes.First();
      Assert.True(first.Fields.ContainsKey("Q"), $"Fields: [{string.Join(", ", first.Fields.Keys)}]");
   }

   [Fact]
   public void LoadAllNotesOfType_sentence_notes_have_expected_fields()
   {
      var result = NoteBulkLoader.LoadAllNotesOfType(TestDbPath, NoteTypes.Sentence, g => new SentenceId(g));
      var first = result.Notes.First();
      Assert.True(first.Fields.ContainsKey("Q"), $"Fields: [{string.Join(", ", first.Fields.Keys)}]");
   }

   // ── CardStudyingStatusLoader ──

   [Fact]
   public void FetchAll_returns_studying_statuses()
   {
      var statuses = CardStudyingStatusLoader.FetchAll(TestDbPath);
      Assert.NotEmpty(statuses);
   }

   [Fact]
   public void FetchAll_returns_statuses_for_all_note_types()
   {
      var statuses = CardStudyingStatusLoader.FetchAll(TestDbPath);

      var noteTypes = statuses.Select(s => s.NoteTypeName).Distinct().ToList();
      Assert.Contains(NoteTypes.Vocab, noteTypes);
      Assert.Contains(NoteTypes.Kanji, noteTypes);
      Assert.Contains(NoteTypes.Sentence, noteTypes);
   }

   [Fact]
   public void FetchAll_statuses_have_valid_data()
   {
      var statuses = CardStudyingStatusLoader.FetchAll(TestDbPath);
      Assert.All(statuses, s =>
      {
         Assert.True(s.AnkiNoteId > 0);
         Assert.False(string.IsNullOrEmpty(s.CardType));
         Assert.False(string.IsNullOrEmpty(s.NoteTypeName));
      });
   }
}
