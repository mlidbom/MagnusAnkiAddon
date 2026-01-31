namespace MagnusCore.Domain;

/// <summary>
/// DTO representing a janome token - pure C# data, no Python dependencies
/// </summary>
public record Token(
    string Surface,
    string BaseForm,
    string PartOfSpeech,
    string Reading,
    string Phonetic,
    string InflectionType,
    string InflectionForm
);
