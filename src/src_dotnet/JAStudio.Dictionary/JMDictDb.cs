using LinqToDB;
using LinqToDB.Data;

namespace JAStudio.Dictionary;

sealed class JMDictDb : DataConnection
{
   JMDictDb(DataOptions options) : base(options) {}

   public ITable<WordKanjiRow> WordKanjis => this.GetTable<WordKanjiRow>();
   public ITable<WordReadingRow> WordReadings => this.GetTable<WordReadingRow>();
   public ITable<WordSenseRow> WordSenses => this.GetTable<WordSenseRow>();

   public ITable<NameKanjiRow> NameKanjis => this.GetTable<NameKanjiRow>();
   public ITable<NameReadingRow> NameReadings => this.GetTable<NameReadingRow>();
   public ITable<NameTranslationRow> NameTranslations => this.GetTable<NameTranslationRow>();

   public static JMDictDb OpenReadOnly(string dbPath) =>
      new(new DataOptions()
         .UseSQLite($"Data Source={dbPath};Mode=ReadOnly"));

   public static JMDictDb Open(string dbPath) =>
      new(new DataOptions()
         .UseSQLite($"Data Source={dbPath}"));
}
