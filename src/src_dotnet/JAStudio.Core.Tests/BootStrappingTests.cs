using Xunit;

namespace JAStudio.Core.Tests;

public class BootStrappingTests
{
   [Fact]
   public void BootstrappingSmokeTest()
   {
      using var _ = App.Bootstrap();
   }

   [Fact]
   public void Can_resolve_all_registered_services()
   {
      using var app = App.Bootstrap();
      var services = app.Services;

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
