namespace JAStudio.Core.Storage.Media;

public record VocabMediaImportRule(
   SourceTag Prefix,
   MediaImportRoute AudioFirst,
   MediaImportRoute AudioSecond,
   MediaImportRoute AudioTts,
   MediaImportRoute Image,
   MediaImportRoute UserImage) : IMediaImportRule;
