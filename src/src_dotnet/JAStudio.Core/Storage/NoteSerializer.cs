using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Threading.Tasks;
using JAStudio.Core.Note;
using JAStudio.Core.Storage.Converters;
using JAStudio.Core.Storage.Dto;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Storage;

public class NoteSerializer
{
   static readonly JsonSerializerOptions JsonOptions = new()
                                                       {
                                                          WriteIndented = true,
                                                          PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                                                          Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
                                                       };

   /// <summary>Compact (non-indented) options for snapshot files — never human-read, ~40% smaller than indented.</summary>
   static readonly JsonSerializerOptions CompactJsonOptions = new()
                                                              {
                                                                 PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                                                                 Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
                                                              };

   readonly NoteServices _noteServices;

   public NoteSerializer(NoteServices noteServices) => _noteServices = noteServices;

   // --- Individual note serialization (indented, for individual files) ---

   public string Serialize(KanjiNote note) => JsonSerializer.Serialize(KanjiNoteConverter.ToDto(note), JsonOptions);
   public string Serialize(VocabNote note) => JsonSerializer.Serialize(VocabNoteConverter.ToDto(note), JsonOptions);
   public string Serialize(SentenceNote note) => JsonSerializer.Serialize(SentenceNoteConverter.ToDto(note), JsonOptions);

   public string Serialize(AllNotesData data)
   {
      var container = new AllNotesContainer
                      {
                         Kanji = data.Kanji.Select(KanjiNoteConverter.ToDto).ToList(),
                         Vocab = data.Vocab.Select(VocabNoteConverter.ToDto).ToList(),
                         Sentences = data.Sentences.Select(SentenceNoteConverter.ToDto).ToList(),
                      };
      return JsonSerializer.Serialize(container, JsonOptions);
   }

   // --- Individual note deserialization (from string, for individual files) ---

   public KanjiNote DeserializeKanji(string json)
   {
      var dto = JsonSerializer.Deserialize<KanjiNoteDto>(json, JsonOptions)
             ?? throw new JsonException("Failed to deserialize KanjiNoteDto");
      return new KanjiNote(_noteServices, KanjiNoteConverter.FromDto(dto));
   }

   public VocabNote DeserializeVocab(string json)
   {
      var dto = JsonSerializer.Deserialize<VocabNoteDto>(json, JsonOptions)
             ?? throw new JsonException("Failed to deserialize VocabNoteDto");
      return new VocabNote(_noteServices, VocabNoteConverter.FromDto(dto));
   }

   public SentenceNote DeserializeSentence(string json)
   {
      var dto = JsonSerializer.Deserialize<SentenceNoteDto>(json, JsonOptions)
             ?? throw new JsonException("Failed to deserialize SentenceNoteDto");
      return new SentenceNote(_noteServices, SentenceNoteConverter.FromDto(dto));
   }

   // --- Legacy: all-in-one-string (kept for test compatibility with SaveAllSingleFile/LoadAllSingleFile) ---

   public AllNotesData DeserializeAll(string json)
   {
      using var runner = _noteServices.TaskRunner.Current("Processing snapshot data");
      var container = runner.RunOnBackgroundThreadWithSpinningProgressDialog("Deserializing snapshot data", () => JsonSerializer.Deserialize<AllNotesContainer>(json, JsonOptions) ?? throw new JsonException("Failed to deserialize snapshot"));

      var threads = ThreadCount.FractionOfLogicalCores(0.2);
      var kanji = runner.ProcessWithProgressAsync(container.Kanji, dto => new KanjiNote(_noteServices, KanjiNoteConverter.FromDto(dto)), "constructing kanji", threads);
      var vocab = runner.ProcessWithProgressAsync(container.Vocab, dto => new VocabNote(_noteServices, VocabNoteConverter.FromDto(dto)), "constructing vocab", threads);
      var sentences = runner.ProcessWithProgressAsync(container.Sentences, dto => new SentenceNote(_noteServices, SentenceNoteConverter.FromDto(dto)), "constructing sentences", threads);

      return new AllNotesData(kanji.Result, vocab.Result, sentences.Result);
   }

   // --- Streaming snapshot: per-type file I/O ---

   /// <summary>
   /// Stream-based per-element deserialization. Reads the JSON array one element at a time,
   /// constructing each note immediately — never materializing the entire DTO list in memory.
   /// </summary>
   public Task<List<KanjiNote>> DeserializeKanjiStreamAsync(Stream stream) =>
      DeserializeStreamAsync<KanjiNote, KanjiNoteDto>(stream, KanjiNoteConverter.FromDto, (s, d) => new KanjiNote(s, d));

   public Task<List<VocabNote>> DeserializeVocabStreamAsync(Stream stream) =>
      DeserializeStreamAsync<VocabNote, VocabNoteDto>(stream, VocabNoteConverter.FromDto, (s, d) => new VocabNote(s, d));

   public Task<List<SentenceNote>> DeserializeSentenceStreamAsync(Stream stream) =>
      DeserializeStreamAsync<SentenceNote, SentenceNoteDto>(stream, SentenceNoteConverter.FromDto, (s, d) => new SentenceNote(s, d));

   async Task<List<TNote>> DeserializeStreamAsync<TNote, TDto>(
      Stream stream,
      Func<TDto, NoteData> fromDto,
      Func<NoteServices, NoteData, TNote> noteConstructor) where TDto : class
   {
      var notes = new List<TNote>();
      await foreach(var dto in JsonSerializer.DeserializeAsyncEnumerable<TDto>(stream, CompactJsonOptions))
      {
         if(dto == null) continue;
         notes.Add(noteConstructor(_noteServices, fromDto(dto)));
      }

      return notes;
   }

   /// <summary>
   /// Streaming serialization — writes each note as a JSON array element directly to the stream
   /// via Utf8JsonWriter, never building a giant intermediate string or DTO list.
   /// </summary>
   public void SerializeKanjiToStream(List<KanjiNote> notes, Stream stream) =>
      SerializeToStream(notes, stream, KanjiNoteConverter.ToDto);

   public void SerializeVocabToStream(List<VocabNote> notes, Stream stream) =>
      SerializeToStream(notes, stream, VocabNoteConverter.ToDto);

   public void SerializeSentenceToStream(List<SentenceNote> notes, Stream stream) =>
      SerializeToStream(notes, stream, SentenceNoteConverter.ToDto);

   static void SerializeToStream<TNote, TDto>(List<TNote> notes, Stream stream, Func<TNote, TDto> toDto)
   {
      using var writer = new Utf8JsonWriter(stream);
      writer.WriteStartArray();
      foreach(var note in notes)
      {
         JsonSerializer.Serialize(writer, toDto(note), CompactJsonOptions);
      }

      writer.WriteEndArray();
      writer.Flush();
   }

   // Internal container — keeps DTOs out of the public API
   class AllNotesContainer
   {
      public List<KanjiNoteDto> Kanji { get; set; } = [];
      public List<VocabNoteDto> Vocab { get; set; } = [];
      public List<SentenceNoteDto> Sentences { get; set; } = [];
   }
}
