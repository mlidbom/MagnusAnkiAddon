using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Core.Anki;
using JAStudio.Core.Note;
using JAStudio.Core.Storage;
using JAStudio.Core.TaskRunners;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Storage;

/// <summary>
/// TEMPORARY test: loads vocab notes from both Anki SQLite and the filesystem repository,
/// then compares every field to identify discrepancies. Delete after debugging.
/// </summary>
public class AnkiVsFileSystemComparisonTests : TestStartingWithEmptyCollection
{
   static readonly string TestDbPath =
      Environment.GetEnvironmentVariable("ANKI_TEST_DB_PATH")
      ?? Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "tests", "collection.anki2"));

   static readonly string JasDatabaseDir =
      Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "jas_database"));

   [Fact]
   public void VocabNotes_AnkiAndFileSystem_HaveIdenticalFields()
   {
      // --- Load from Anki ---
      var ankiBulk = NoteBulkLoader.LoadAllNotesOfType(TestDbPath, NoteTypes.Vocab, g => new VocabId(g));
      var serializer = GetService<NoteSerializer>();
      var ankiNotes = ankiBulk.Notes
         .Select(nd => new VocabNote(NoteServices, nd))
         .ToDictionary(n => n.GetId());

      // --- Load from filesystem ---
      var repo = new FileSystemNoteRepository(serializer, GetService<TaskRunner>(), JasDatabaseDir);
      var fsNotes = repo.LoadAll().Vocab.ToDictionary(n => n.GetId());

      Console.WriteLine($"Anki: {ankiNotes.Count} vocab notes, FileSystem: {fsNotes.Count} vocab notes");

      // --- Check counts ---
      var missingInFs = ankiNotes.Keys.Except(fsNotes.Keys).ToList();
      var missingInAnki = fsNotes.Keys.Except(ankiNotes.Keys).ToList();

      foreach (var id in missingInFs)
         Console.WriteLine($"MISSING in filesystem: {id} (Q: {ankiNotes[id].GetQuestion()})");
      foreach (var id in missingInAnki)
         Console.WriteLine($"MISSING in Anki: {id}");

      // --- Compare fields for notes present in both ---
      var commonIds = ankiNotes.Keys.Intersect(fsNotes.Keys).ToList();
      var differences = new List<string>();

      foreach (var id in commonIds)
      {
         var ankiData = ankiNotes[id].GetData();
         var fsData = fsNotes[id].GetData();

         // Compare all fields from Anki
         foreach (var kvp in ankiData.Fields)
         {
            var ankiValue = kvp.Value;
            var fsValue = fsData.Fields.TryGetValue(kvp.Key, out var v) ? v : "<MISSING>";

            if (ankiValue != fsValue)
            {
               // Skip known benign differences
               if (kvp.Key == "sentence_count" && IsEffectivelyEmpty(ankiValue) && IsEffectivelyEmpty(fsValue))
                  continue;

               var diff = $"Note {ankiData.Id} (Q: {Truncate(ankiNotes[id].GetQuestion(), 30)}): " +
                          $"Field '{kvp.Key}' differs\n" +
                          $"  Anki: [{Truncate(ankiValue, 100)}]\n" +
                          $"  FS:   [{Truncate(fsValue, 100)}]";
               differences.Add(diff);
               Console.WriteLine(diff);
            }
         }

         // Check for fields in filesystem that aren't in Anki
         foreach (var kvp in fsData.Fields.Where(f => !string.IsNullOrEmpty(f.Value)))
         {
            if (!ankiData.Fields.ContainsKey(kvp.Key))
            {
               var diff = $"Note {fsData.Id} (Q: {Truncate(fsNotes[id].GetQuestion(), 30)}): " +
                          $"Field '{kvp.Key}' exists in FS but not in Anki\n" +
                          $"  FS value: [{Truncate(kvp.Value, 100)}]";
               differences.Add(diff);
               Console.WriteLine(diff);
            }
         }

         // Compare tags
         var ankiTags = ankiData.Tags.OrderBy(t => t).ToList();
         var fsTags = fsData.Tags.OrderBy(t => t).ToList();
         if (!ankiTags.SequenceEqual(fsTags))
         {
            var diff = $"Note {ankiData.Id} (Q: {Truncate(ankiNotes[id].GetQuestion(), 30)}): " +
                       $"Tags differ\n" +
                       $"  Anki: [{string.Join(", ", ankiTags)}]\n" +
                       $"  FS:   [{string.Join(", ", fsTags)}]";
            differences.Add(diff);
            Console.WriteLine(diff);
         }
      }

      Console.WriteLine($"\nSummary: {commonIds.Count} notes compared, {differences.Count} field differences found");
      Console.WriteLine($"  Missing in filesystem: {missingInFs.Count}");
      Console.WriteLine($"  Missing in Anki: {missingInAnki.Count}");

      var reportPath = Path.Combine(Path.GetTempPath(), "anki_vs_fs_diff.txt");
      var reportLines = new List<string>();

      try
      {
         reportLines.Add($"Anki notes: {ankiNotes.Count}, FS notes: {fsNotes.Count}");
         reportLines.Add($"Common IDs: {ankiNotes.Keys.Intersect(fsNotes.Keys).Count()}");
         reportLines.Add($"Missing in filesystem: {missingInFs.Count}");
         reportLines.Add($"Missing in Anki: {missingInAnki.Count}");
         reportLines.Add("");

         reportLines.Add("--- Sample Anki IDs ---");
         foreach (var n in ankiNotes.Values.Take(5))
            reportLines.Add($"  {n.GetId()} {n.GetId().Value} Q: {n.GetQuestion()}");
         reportLines.Add("");
         reportLines.Add("--- Sample FS IDs ---");
         foreach (var n in fsNotes.Values.Take(5))
            reportLines.Add($"  {n.GetId()} {n.GetId().Value} Q: {n.GetQuestion()}");
         reportLines.Add("");

         // Try matching by question text instead (handle duplicate questions)
         var ankiByQ = ankiNotes.Values.GroupBy(n => n.GetQuestion()).ToDictionary(g => g.Key, g => g.First());
         var fsByQ = fsNotes.Values.GroupBy(n => n.GetQuestion()).ToDictionary(g => g.Key, g => g.First());
         var commonByQ = ankiByQ.Keys.Intersect(fsByQ.Keys).ToList();
         reportLines.Add($"--- Match by question text: {commonByQ.Count} common ---");

         foreach (var q in commonByQ.Take(10))
         {
            var ankiN = ankiByQ[q];
            var fsN = fsByQ[q];
            reportLines.Add($"  Q: {Truncate(q, 30)}  Anki ID: {ankiN.GetId().Value}  FS ID: {fsN.GetId().Value}  Match: {ankiN.GetId() == fsN.GetId()}");

            // Compare fields for these matched notes
            var ankiData = ankiN.GetData();
            var fsData = fsN.GetData();
            foreach (var kvp in ankiData.Fields)
            {
               var ankiVal = kvp.Value;
               var fsVal = fsData.Fields.TryGetValue(kvp.Key, out var v) ? v : "<MISSING>";
               if (ankiVal != fsVal && !(kvp.Key == "sentence_count" && IsEffectivelyEmpty(ankiVal) && IsEffectivelyEmpty(fsVal)))
               {
                  reportLines.Add($"    DIFF field '{kvp.Key}': Anki=[{Truncate(ankiVal, 80)}] FS=[{Truncate(fsVal, 80)}]");
               }
            }
         }
      }
      catch (Exception ex)
      {
         reportLines.Add($"EXCEPTION: {ex}");
      }

      File.WriteAllText(reportPath, string.Join("\n", reportLines), System.Text.Encoding.UTF8);

      Assert.True(differences.Count == 0 && missingInFs.Count == 0 && missingInAnki.Count == 0,
         $"{differences.Count} differences, {missingInFs.Count} missing in FS, {missingInAnki.Count} missing in Anki. Report: {reportPath}");
   }

   static bool IsEffectivelyEmpty(string value) => string.IsNullOrEmpty(value) || value == "0";
   static string Truncate(string value, int maxLength) => value.Length <= maxLength ? value : value[..maxLength] + "...";
}
