namespace JAStudio.Core.Storage.Media;

public record SentenceMediaImportRule(
   SourceTag Prefix,
   MediaImportRoute Audio,
   MediaImportRoute Screenshot) : IMediaImportRule;
