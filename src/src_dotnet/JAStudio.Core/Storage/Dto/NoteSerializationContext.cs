using System.Text.Json.Serialization;

namespace JAStudio.Core.Storage.Dto;

/// <summary>
/// Source-generated JSON serialization context for all note DTOs.
/// Eliminates reflection-based serialization at runtime — the compiler generates
/// optimized read/write code for each DTO type at build time.
/// Options (encoder, indenting, naming policy) are supplied at construction time
/// via NoteSerializer so the Encoder (not settable via attribute) can be configured.
/// </summary>
[JsonSerializable(typeof(KanjiNoteDto))]
[JsonSerializable(typeof(VocabNoteDto))]
[JsonSerializable(typeof(VocabMatchingRulesDto))]
[JsonSerializable(typeof(VocabRelatedDataDto))]
[JsonSerializable(typeof(SentenceNoteDto))]
[JsonSerializable(typeof(SentenceConfigurationDto))]
[JsonSerializable(typeof(WordExclusionDto))]
[JsonSerializable(typeof(ParsingResultDto))]
[JsonSerializable(typeof(ParsedMatchDto))]
[JsonSerializable(typeof(AllNotesContainer))]
[JsonSourceGenerationOptions(
   PropertyNamingPolicy = JsonKnownNamingPolicy.CamelCase,
   GenerationMode = JsonSourceGenerationMode.Default)]
internal partial class NoteSerializationContext : JsonSerializerContext;
