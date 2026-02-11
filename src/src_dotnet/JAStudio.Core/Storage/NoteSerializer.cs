using System.Collections.Generic;
using System.Linq;
using System.Text.Encodings.Web;
using System.Text.Json;
using JAStudio.Core.Note;
using JAStudio.Core.Storage.Converters;
using JAStudio.Core.Storage.Dto;

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

    public NoteSerializer(NoteServices noteServices)
    {
        _noteServices = noteServices;
    }

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

    public KanjiNote DeserializeKanji(string json)
    {
        var dto = JsonSerializer.Deserialize<KanjiNoteDto>(json, JsonOptions)
                  ?? throw new JsonException("Failed to deserialize KanjiNoteDto");
        var noteData = KanjiNoteConverter.FromDto(dto);
        return new KanjiNote(_noteServices, noteData);
    }

    public VocabNote DeserializeVocab(string json)
    {
        var dto = JsonSerializer.Deserialize<VocabNoteDto>(json, JsonOptions)
                  ?? throw new JsonException("Failed to deserialize VocabNoteDto");
        var noteData = VocabNoteConverter.FromDto(dto);
        return new VocabNote(_noteServices, noteData);
    }

    public SentenceNote DeserializeSentence(string json)
    {
        var dto = JsonSerializer.Deserialize<SentenceNoteDto>(json, JsonOptions)
                  ?? throw new JsonException("Failed to deserialize SentenceNoteDto");
        var noteData = SentenceNoteConverter.FromDto(dto);
        return new SentenceNote(_noteServices, noteData);
    }

    public AllNotesData DeserializeAll(string json)
    {
        var container = JsonSerializer.Deserialize<AllNotesContainer>(json, JsonOptions)
                        ?? throw new JsonException("Failed to deserialize AllNotesData");

        var kanji = container.Kanji.Select(dto => new KanjiNote(_noteServices, KanjiNoteConverter.FromDto(dto))).ToList();
        var vocab = container.Vocab.Select(dto => new VocabNote(_noteServices, VocabNoteConverter.FromDto(dto))).ToList();
        var sentences = container.Sentences.Select(dto => new SentenceNote(_noteServices, SentenceNoteConverter.FromDto(dto))).ToList();

        return new AllNotesData(kanji, vocab, sentences);
    }
}
