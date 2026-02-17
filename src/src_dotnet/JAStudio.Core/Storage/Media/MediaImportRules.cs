namespace JAStudio.Core.Storage.Media;

public record VocabImportRule(SourceTag Prefix, VocabMediaField Field, string TargetDirectory, CopyrightStatus Copyright);
public record SentenceImportRule(SourceTag Prefix, SentenceMediaField Field, string TargetDirectory, CopyrightStatus Copyright);
public record KanjiImportRule(SourceTag Prefix, KanjiMediaField Field, string TargetDirectory, CopyrightStatus Copyright);
