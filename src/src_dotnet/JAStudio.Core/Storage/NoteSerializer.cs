using System.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;
using JAStudio.Core.Note;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
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
                                                          TypeInfoResolver = new NoteSerializationContext(new JsonSerializerOptions
                                                                                                          {
                                                                                                             PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                                                                                                             Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
                                                                                                          }),
                                                       };

   readonly NoteServices _noteServices;

   public NoteSerializer(NoteServices noteServices) => _noteServices = noteServices;

   public string Serialize(KanjiNote note) => JsonSerializer.Serialize(KanjiNoteConverter.ToCorpusData(note), JsonOptions);
   public string Serialize(VocabNote note) => JsonSerializer.Serialize(VocabNoteConverter.ToCorpusData(note), JsonOptions);
   public string Serialize(SentenceNote note) => JsonSerializer.Serialize(SentenceNoteConverter.ToCorpusData(note), JsonOptions);

   public string Serialize(AllNotesData data)
   {
      var container = new AllNotesContainer
                      {
                         Kanji = data.Kanji.Select(KanjiNoteConverter.ToCorpusData).ToList(),
                         Vocab = data.Vocab.Select(VocabNoteConverter.ToCorpusData).ToList(),
                         Sentences = data.Sentences.Select(SentenceNoteConverter.ToCorpusData).ToList(),
                      };
      return JsonSerializer.Serialize(container, JsonOptions);
   }

   public KanjiNote DeserializeKanji(string json)
   {
      var data = JsonSerializer.Deserialize<KanjiData>(json, JsonOptions)
             ?? throw new JsonException("Failed to deserialize KanjiData");
      return new KanjiNote(_noteServices, data);
   }

   public VocabNote DeserializeVocab(string json)
   {
      var data = JsonSerializer.Deserialize<VocabData>(json, JsonOptions)
             ?? throw new JsonException("Failed to deserialize VocabData");
      return new VocabNote(_noteServices, data);
   }

   public SentenceNote DeserializeSentence(string json)
   {
      var data = JsonSerializer.Deserialize<SentenceData>(json, JsonOptions)
             ?? throw new JsonException("Failed to deserialize SentenceData");
      return new SentenceNote(_noteServices, data);
   }

   public AllNotesData DeserializeAll(string json)
   {
      var container = JsonSerializer.Deserialize<AllNotesContainer>(json, JsonOptions)
                   ?? throw new JsonException("Failed to deserialize AllNotesData");

      return ContainerToAllNotesData(container);
   }

   internal KanjiData DeserializeKanjiToData(string json) =>
      JsonSerializer.Deserialize<KanjiData>(json, JsonOptions)
   ?? throw new JsonException("Failed to deserialize KanjiData");

   internal VocabData DeserializeVocabToData(string json) =>
      JsonSerializer.Deserialize<VocabData>(json, JsonOptions)
   ?? throw new JsonException("Failed to deserialize VocabData");

   internal SentenceData DeserializeSentenceToData(string json) =>
      JsonSerializer.Deserialize<SentenceData>(json, JsonOptions)
   ?? throw new JsonException("Failed to deserialize SentenceData");

   internal AllNotesContainer AllNotesDataToContainer(AllNotesData data) => new()
                                                                            {
                                                                               Kanji = data.Kanji.Select(KanjiNoteConverter.ToCorpusData).ToList(),
                                                                               Vocab = data.Vocab.Select(VocabNoteConverter.ToCorpusData).ToList(),
                                                                               Sentences = data.Sentences.Select(SentenceNoteConverter.ToCorpusData).ToList(),
                                                                            };

   internal AllNotesData ContainerToAllNotesData(AllNotesContainer container)
   {
      using var runner = _noteServices.TaskRunner.Current("Converting snapshot to notes");
      var kanji = runner.RunBatchAsync(container.Kanji, data => new KanjiNote(_noteServices, data), "Constructing kanji notes");
      var vocab = runner.RunBatchAsync(container.Vocab, data => new VocabNote(_noteServices, data), "Constructing vocab notes", ThreadCount.FractionOfLogicalCores(0.15));
      var sentences = runner.RunBatchAsync(container.Sentences, data => new SentenceNote(_noteServices, data), "Constructing sentence notes", ThreadCount.FractionOfLogicalCores(0.3));

      return new AllNotesData(kanji.Result.ToList(), vocab.Result.ToList(), sentences.Result.ToList());
   }
}
