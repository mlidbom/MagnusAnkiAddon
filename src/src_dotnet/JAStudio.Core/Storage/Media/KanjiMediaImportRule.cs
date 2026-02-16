namespace JAStudio.Core.Storage.Media;

public record KanjiMediaImportRule(
   SourceTag Prefix,
   MediaImportRoute Audio,
   MediaImportRoute Image) : IMediaImportRule;
