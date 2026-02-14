using System;
using System.Collections.Generic;
using MemoryPack;

namespace JAStudio.Core.Storage.Dto;

[MemoryPackable]
public partial class SentenceNoteDto
{
    public Guid Id { get; set; }
    public string SourceQuestion { get; set; } = string.Empty;
    public string UserQuestion { get; set; } = string.Empty;
    public string ActiveQuestion { get; set; } = string.Empty;
    public string SourceAnswer { get; set; } = string.Empty;
    public string UserAnswer { get; set; } = string.Empty;
    public string ActiveAnswer { get; set; } = string.Empty;
    public string SourceComments { get; set; } = string.Empty;
    public string UserComments { get; set; } = string.Empty;
    public string Reading { get; set; } = string.Empty;
    public string ExternalId { get; set; } = string.Empty;
    public string Audio { get; set; } = string.Empty;
    public string Screenshot { get; set; } = string.Empty;
    public SentenceConfigurationDto Configuration { get; set; } = new();
    public ParsingResultDto? ParsingResult { get; set; }
    public string JanomeTokens { get; set; } = string.Empty;
    public List<string> Tags { get; set; } = new();
}

[MemoryPackable]
public partial class SentenceConfigurationDto
{
    public List<string> HighlightedWords { get; set; } = new();
    public List<WordExclusionDto> IncorrectMatches { get; set; } = new();
    public List<WordExclusionDto> HiddenMatches { get; set; } = new();
}

[MemoryPackable]
public partial class WordExclusionDto
{
    public string Word { get; set; } = string.Empty;
    public int Index { get; set; } = -1;
}

[MemoryPackable]
public partial class ParsingResultDto
{
    public string Sentence { get; set; } = string.Empty;
    public string ParserVersion { get; set; } = string.Empty;
    public List<ParsedMatchDto> ParsedWords { get; set; } = new();
}

[MemoryPackable]
public partial class ParsedMatchDto
{
    public string Variant { get; set; } = string.Empty;
    public int StartIndex { get; set; }
    public bool IsDisplayed { get; set; }
    public string ParsedForm { get; set; } = string.Empty;
    public Guid? VocabId { get; set; }
}
