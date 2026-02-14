using System;
using System.Collections.Generic;
using MemoryPack;

namespace JAStudio.Core.Storage.Dto;

[MemoryPackable]
public partial class VocabNoteDto
{
    public Guid Id { get; set; }
    public string Question { get; set; } = string.Empty;
    public string SourceAnswer { get; set; } = string.Empty;
    public string UserAnswer { get; set; } = string.Empty;
    public string ActiveAnswer { get; set; } = string.Empty;
    public string UserExplanation { get; set; } = string.Empty;
    public string UserExplanationLong { get; set; } = string.Empty;
    public string UserMnemonic { get; set; } = string.Empty;
    public List<string> UserCompounds { get; set; } = new();
    public List<string> Readings { get; set; } = new();
    public string PartsOfSpeech { get; set; } = string.Empty;
    public string ParsedTypeOfSpeech { get; set; } = string.Empty;
    public string SourceMnemonic { get; set; } = string.Empty;
    public string SourceReadingMnemonic { get; set; } = string.Empty;
    public string AudioB { get; set; } = string.Empty;
    public string AudioG { get; set; } = string.Empty;
    public string AudioTTS { get; set; } = string.Empty;
    public string Kanji { get; set; } = string.Empty;
    public List<string> Forms { get; set; } = new();
    public string Homophones { get; set; } = string.Empty;
    public int SentenceCount { get; set; }
    public VocabMatchingRulesDto MatchingRules { get; set; } = new();
    public VocabRelatedDataDto RelatedVocab { get; set; } = new();
    public List<string> Tags { get; set; } = new();
}

[MemoryPackable]
public partial class VocabMatchingRulesDto
{
    public List<string> PrefixIsNot { get; set; } = new();
    public List<string> SuffixIsNot { get; set; } = new();
    public List<string> SurfaceIsNot { get; set; } = new();
    public List<string> YieldToSurface { get; set; } = new();
    public List<string> RequiredPrefix { get; set; } = new();
}

[MemoryPackable]
public partial class VocabRelatedDataDto
{
    public string ErgativeTwin { get; set; } = string.Empty;
    public string DerivedFrom { get; set; } = string.Empty;
    public List<string> PerfectSynonyms { get; set; } = new();
    public List<string> Synonyms { get; set; } = new();
    public List<string> Antonyms { get; set; } = new();
    public List<string> ConfusedWith { get; set; } = new();
    public List<string> SeeAlso { get; set; } = new();
}
