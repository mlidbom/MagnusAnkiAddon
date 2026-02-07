using JAStudio.Core.Note;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests;

public class BootStrappingTests : TestStartingWithEmptyCollection
{
   [Fact]
   public void Can_resolve_all_registered_services()
   {
      var services = TemporaryServiceCollection.Instance;

      // Verify every service in TemporaryServiceCollection resolves without throwing
      Assert.NotNull(services.App);
      Assert.NotNull(services.ConfigurationStore);
      Assert.NotNull(services.Settings);
      Assert.NotNull(services.QueryBuilder);

      // Core services
      Assert.NotNull(services.LocalNoteUpdater);
      Assert.NotNull(services.TaskRunner);
      Assert.NotNull(services.AnkiCardOperations);
      Assert.NotNull(services.DictLookup);
      Assert.NotNull(services.TestApp);

      // Note services
      Assert.NotNull(services.KanjiNoteMnemonicMaker);
      Assert.NotNull(services.VocabNoteFactory);
      Assert.NotNull(services.VocabNoteGeneratedData);

      // ViewModels
      Assert.NotNull(services.SentenceKanjiListViewModel);

      // Renderers
      Assert.NotNull(services.KanjiListRenderer);
      Assert.NotNull(services.VocabKanjiListRenderer);
      Assert.NotNull(services.RelatedVocabsRenderer);
      Assert.NotNull(services.UdSentenceBreakdownRenderer);
      Assert.NotNull(services.QuestionRenderer);
      Assert.NotNull(services.SentenceRenderer);
   }
}
