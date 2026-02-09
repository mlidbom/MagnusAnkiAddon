using System;
using System.Collections.Generic;

namespace JAStudio.Core.Storage.Dto;

public class KanjiNoteDto
{
    public Guid Id { get; set; }
    public string Kanji { get; set; } = string.Empty;
    public string SourceAnswer { get; set; } = string.Empty;
    public string UserAnswer { get; set; } = string.Empty;
    public string ActiveAnswer { get; set; } = string.Empty;
    public string ReadingOnHtml { get; set; } = string.Empty;
    public string ReadingKunHtml { get; set; } = string.Empty;
    public string ReadingNanHtml { get; set; } = string.Empty;
    public List<string> Radicals { get; set; } = new();
    public string SourceMeaningMnemonic { get; set; } = string.Empty;
    public string MeaningInfo { get; set; } = string.Empty;
    public string ReadingMnemonic { get; set; } = string.Empty;
    public string ReadingInfo { get; set; } = string.Empty;
    public List<string> PrimaryVocab { get; set; } = new();
    public string Audio { get; set; } = string.Empty;
    public string UserMnemonic { get; set; } = string.Empty;
    public List<string> SimilarMeaning { get; set; } = new();
    public List<string> ConfusedWith { get; set; } = new();
    public List<string> Tags { get; set; } = new();
}
