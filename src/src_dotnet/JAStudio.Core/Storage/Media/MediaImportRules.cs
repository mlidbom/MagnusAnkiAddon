namespace JAStudio.Core.Storage.Media;

public class VocabImportRule(SourceTag prefix, VocabMediaField field, string targetDirectory, CopyrightStatus copyright)
{
   public SourceTag Prefix { get; } = prefix;
   public VocabMediaField Field { get; } = field;
   public string TargetDirectory { get; } = targetDirectory;
   public CopyrightStatus Copyright { get; } = copyright;
}

public class SentenceImportRule(SourceTag prefix, SentenceMediaField field, string targetDirectory, CopyrightStatus copyright)
{
   public SourceTag Prefix { get; } = prefix;
   public SentenceMediaField Field { get; } = field;
   public string TargetDirectory { get; } = targetDirectory;
   public CopyrightStatus Copyright { get; } = copyright;
}

public class KanjiImportRule(SourceTag prefix, KanjiMediaField field, string targetDirectory, CopyrightStatus copyright)
{
   public SourceTag Prefix { get; } = prefix;
   public KanjiMediaField Field { get; } = field;
   public string TargetDirectory { get; } = targetDirectory;
   public CopyrightStatus Copyright { get; } = copyright;
}
