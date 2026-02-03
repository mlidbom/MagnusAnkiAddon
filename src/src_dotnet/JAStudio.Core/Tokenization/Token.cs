namespace JAStudio.Core.Tokenization;

public record Token(
    string Surface,
    string BaseForm,
    string PartOfSpeech,
    string Reading,
    string Phonetic,
    string InflectionType,
    string InflectionForm
);
