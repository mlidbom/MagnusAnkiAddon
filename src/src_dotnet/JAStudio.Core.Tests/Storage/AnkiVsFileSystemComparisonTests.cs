using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using JAStudio.Anki;
using JAStudio.Core.Note;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage;
using JAStudio.Core.TaskRunners;
using Xunit;

namespace JAStudio.Core.Tests.Storage;

/// <summary>
/// TEMPORARY test: loads vocab notes from both Anki SQLite and the filesystem repository,
/// then compares raw fields AND parsed structured data to identify discrepancies. Delete after debugging.
/// </summary>
public class AnkiVsFileSystemComparisonTests : Specification_for_an_empty_collection
{
   static readonly string TestDbPath =
      Environment.GetEnvironmentVariable("ANKI_TEST_DB_PATH")
   ?? Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "tests", "collection.anki2"));

   static readonly string JasDatabaseDir =
      Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "jas_database"));

   static readonly HashSet<string> IgnoredFields = [];

   [Fact(Skip = "This test was to explore a problem that probably does not actually exist, will most likely be removed soon.")]
   public void VocabNotes_AnkiAndFileSystem_HaveIdenticalData()
   {
      // --- Load from Anki ---
      var ankiBulk = NoteBulkLoader.LoadAllNotesOfType(TestDbPath, NoteTypes.Vocab, g => new VocabId(g));
      var serializer = GetService<NoteSerializer>();
      var ankiNotes = ankiBulk.Notes
                              .Select(nd => new VocabNote(NoteServices, VocabData.FromAnkiNoteData(nd)))
                              .ToDictionary(n => n.GetId());

      // --- Load from filesystem ---
      var repo = new FileSystemNoteRepository(serializer, GetService<TaskRunner>(), JasDatabaseDir);
      var fsNotes = repo.LoadAll().Vocab.ToDictionary(n => n.GetId());

      // --- Match and compare ---
      var commonIds = ankiNotes.Keys.Intersect(fsNotes.Keys).OrderBy(id => id.Value).ToList();
      var differences = new List<string>();

      foreach(var id in commonIds)
      {
         var anki = ankiNotes[id];
         var fs = fsNotes[id];
         var q = Truncate(anki.GetQuestion(), 30);

         // --- Raw field comparison (skip benign fields) ---
         var ankiData = anki.GetData();
         var fsData = fs.GetData();

         foreach(var kvp in ankiData.Fields)
         {
            if(IgnoredFields.Contains(kvp.Key)) continue;
            var ankiVal = kvp.Value;
            var fsVal = fsData.Fields.TryGetValue(kvp.Key, out var v) ? v : "<MISSING>";
            if(ankiVal != fsVal && !(kvp.Key == "sentence_count" && IsEffectivelyEmpty(ankiVal) && IsEffectivelyEmpty(fsVal)))
               differences.Add($"[{id}] {q}: FIELD '{kvp.Key}'\n  Anki: [{Truncate(ankiVal, 200)}]\n  FS:   [{Truncate(fsVal, 200)}]");
         }

         // --- Tags ---
         var ankiTags = ankiData.Tags.OrderBy(t => t).ToList();
         var fsTags = fsData.Tags.OrderBy(t => t).ToList();
         if(!ankiTags.SequenceEqual(fsTags))
            differences.Add($"[{id}] {q}: TAGS\n  Anki: [{string.Join(", ", ankiTags)}]\n  FS:   [{string.Join(", ", fsTags)}]");

         // --- Parsed structured data ---
         CompareList(differences, $"[{id}] {q}", "Readings", anki.GetReadings(), fs.GetReadings());
         CompareList(differences, $"[{id}] {q}", "Forms", anki.Forms.AllList(), fs.Forms.AllList());
         CompareString(differences, $"[{id}] {q}", "Question", anki.GetQuestion(), fs.GetQuestion());
         CompareString(differences, $"[{id}] {q}", "Answer", anki.GetAnswer(), fs.GetAnswer());
         CompareString(differences, $"[{id}] {q}", "SourceAnswer", anki.SourceAnswer.Value, fs.SourceAnswer.Value);
         CompareString(differences, $"[{id}] {q}", "ActiveAnswer", anki.ActiveAnswer.Value, fs.ActiveAnswer.Value);
         CompareString(differences, $"[{id}] {q}", "User.Answer", anki.User.Answer.Value, fs.User.Answer.Value);
         CompareString(differences, $"[{id}] {q}", "User.Mnemonic", anki.User.Mnemonic.Value, fs.User.Mnemonic.Value);
         CompareString(differences, $"[{id}] {q}", "User.Explanation", anki.User.Explanation.Value, fs.User.Explanation.Value);
         CompareString(differences, $"[{id}] {q}", "PartsOfSpeech.Raw", anki.PartsOfSpeech.RawStringValue(), fs.PartsOfSpeech.RawStringValue());

         // --- MatchingRules ---
         var ankiRules = anki.MatchingConfiguration.ConfigurableRules;
         var fsRules = fs.MatchingConfiguration.ConfigurableRules;
         CompareSet(differences, $"[{id}] {q}", "Rules.SurfaceIsNot", ankiRules.SurfaceIsNot, fsRules.SurfaceIsNot);
         CompareSet(differences, $"[{id}] {q}", "Rules.PrefixIsNot", ankiRules.PrefixIsNot, fsRules.PrefixIsNot);
         CompareSet(differences, $"[{id}] {q}", "Rules.SuffixIsNot", ankiRules.SuffixIsNot, fsRules.SuffixIsNot);
         CompareSet(differences, $"[{id}] {q}", "Rules.YieldToSurface", ankiRules.YieldToSurface, fsRules.YieldToSurface);
         CompareSet(differences, $"[{id}] {q}", "Rules.RequiredPrefix", ankiRules.RequiredPrefix, fsRules.RequiredPrefix);

         // --- RelatedVocab ---
         CompareString(differences, $"[{id}] {q}", "Related.ErgativeTwin", anki.RelatedNotes.ErgativeTwin.Get(), fs.RelatedNotes.ErgativeTwin.Get());
         CompareSet(differences, $"[{id}] {q}", "Related.Synonyms", anki.RelatedNotes.Synonyms.Strings(), fs.RelatedNotes.Synonyms.Strings());
         CompareSet(differences, $"[{id}] {q}", "Related.PerfectSynonyms", anki.RelatedNotes.PerfectSynonyms.Get(), fs.RelatedNotes.PerfectSynonyms.Get());
         CompareSet(differences, $"[{id}] {q}", "Related.Antonyms", anki.RelatedNotes.Antonyms.Strings(), fs.RelatedNotes.Antonyms.Strings());
         CompareSet(differences, $"[{id}] {q}", "Related.ConfusedWith", anki.RelatedNotes.ConfusedWith.Get(), fs.RelatedNotes.ConfusedWith.Get());
         CompareSet(differences, $"[{id}] {q}", "Related.SeeAlso", anki.RelatedNotes.SeeAlso.Strings(), fs.RelatedNotes.SeeAlso.Strings());

         // --- RequireForbid flags (the critical matching data) ---
         foreach(var (ankiFlag, fsFlag) in anki.MatchingConfiguration.RequiresForbids.AllFlags
                                               .Zip(fs.MatchingConfiguration.RequiresForbids.AllFlags))
         {
            if(ankiFlag.IsRequired != fsFlag.IsRequired || ankiFlag.IsForbidden != fsFlag.IsForbidden)
               differences.Add($"[{id}] {q}: RequireForbid '{ankiFlag.Name}'\n" +
                               $"  Anki: Required={ankiFlag.IsRequired} Forbidden={ankiFlag.IsForbidden}\n" +
                               $"  FS:   Required={fsFlag.IsRequired} Forbidden={fsFlag.IsForbidden}");
         }

         // --- BoolFlags ---
         CompareBool(differences,
                     $"[{id}] {q}",
                     "IsInflectingWord",
                     anki.MatchingConfiguration.BoolFlags.IsInflectingWord.IsSet(),
                     fs.MatchingConfiguration.BoolFlags.IsInflectingWord.IsSet());
         CompareBool(differences,
                     $"[{id}] {q}",
                     "IsPoisonWord",
                     anki.MatchingConfiguration.BoolFlags.IsPoisonWord.IsSet(),
                     fs.MatchingConfiguration.BoolFlags.IsPoisonWord.IsSet());
      }

      var reportPath = Path.Combine(Path.GetTempPath(), "anki_vs_fs_diff.txt");
      var summary = $"Anki: {ankiNotes.Count}, FS: {fsNotes.Count}, Common: {commonIds.Count}, " +
                    $"Missing in FS: {ankiNotes.Keys.Except(fsNotes.Keys).Count()}, " +
                    $"Missing in Anki: {fsNotes.Keys.Except(ankiNotes.Keys).Count()}, " +
                    $"Differences: {differences.Count}";
      File.WriteAllText(reportPath, summary + "\n\n" + string.Join("\n\n", differences), System.Text.Encoding.UTF8);

      Assert.True(differences.Count == 0, $"{differences.Count} differences. Report: {reportPath}");
   }

   static void CompareString(List<string> diffs, string ctx, string label, string anki, string fs)
   {
      if(anki != fs)
         diffs.Add($"{ctx}: {label}\n  Anki: [{Truncate(anki, 200)}]\n  FS:   [{Truncate(fs, 200)}]");
   }

   static void CompareList(List<string> diffs, string ctx, string label, List<string> anki, List<string> fs)
   {
      if(!anki.SequenceEqual(fs))
         diffs.Add($"{ctx}: {label}\n  Anki: [{string.Join(", ", anki)}]\n  FS:   [{string.Join(", ", fs)}]");
   }

   static void CompareSet(List<string> diffs, string ctx, string label, IEnumerable<string> anki, IEnumerable<string> fs)
   {
      var ankiSorted = anki.OrderBy(s => s).ToList();
      var fsSorted = fs.OrderBy(s => s).ToList();
      if(!ankiSorted.SequenceEqual(fsSorted))
         diffs.Add($"{ctx}: {label}\n  Anki: [{string.Join(", ", ankiSorted)}]\n  FS:   [{string.Join(", ", fsSorted)}]");
   }

   static void CompareBool(List<string> diffs, string ctx, string label, bool anki, bool fs)
   {
      if(anki != fs)
         diffs.Add($"{ctx}: {label}\n  Anki: {anki}\n  FS:   {fs}");
   }

   static bool IsEffectivelyEmpty(string value) => string.IsNullOrEmpty(value) || value == "0";
   static string Truncate(string value, int maxLength) => value.Length <= maxLength ? value : value[..maxLength] + "...";
}
