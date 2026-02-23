using LinqToDB;
using LinqToDB.Data;

namespace JAStudio.Dictionary;

public sealed class JMDictDb : DataConnection
{
   JMDictDb(DataOptions options) : base(options) {}

   public ITable<WordKanji> WordKanjis => this.GetTable<WordKanji>();
   public ITable<WordReading> WordReadings => this.GetTable<WordReading>();
   public ITable<WordSense> WordSenses => this.GetTable<WordSense>();

   public ITable<NameKanji> NameKanjis => this.GetTable<NameKanji>();
   public ITable<NameReading> NameReadings => this.GetTable<NameReading>();
   public ITable<NameTranslation> NameTranslations => this.GetTable<NameTranslation>();

   public static JMDictDb OpenReadOnly(string dbPath) =>
      new(new DataOptions()
         .UseSQLite($"Data Source={dbPath};Mode=ReadOnly"));

   public static JMDictDb Open(string dbPath) =>
      new(new DataOptions()
         .UseSQLite($"Data Source={dbPath}"));
}
