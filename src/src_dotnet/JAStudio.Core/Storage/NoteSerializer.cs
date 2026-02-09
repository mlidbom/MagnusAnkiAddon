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
    };

    readonly NoteServices _noteServices;

    public NoteSerializer(NoteServices noteServices)
    {
        _noteServices = noteServices;
    }

    public string Serialize(KanjiNote note) => JsonSerializer.Serialize(KanjiNoteConverter.ToDto(note), JsonOptions);
    public string Serialize(VocabNote note) => JsonSerializer.Serialize(VocabNoteConverter.ToDto(note), JsonOptions);
    public string Serialize(SentenceNote note) => JsonSerializer.Serialize(SentenceNoteConverter.ToDto(note), JsonOptions);

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
}
