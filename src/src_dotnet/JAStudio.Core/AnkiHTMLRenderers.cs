using Compze.Utilities.DependencyInjection.Abstractions;
using JAStudio.Core.UI.Web.Kanji;
using JAStudio.Core.UI.Web.Sentence;
using JAStudio.Core.UI.Web.Vocab;

namespace JAStudio.Core;

public class AnkiHTMLRenderers
{
   readonly IServiceLocator _serviceLocator;
   internal AnkiHTMLRenderers(IServiceLocator serviceLocator) => _serviceLocator = serviceLocator;

   // ReSharper disable once UnusedMember.Global used from python
   public VocabNoteRenderer VocabNoteRenderer => _serviceLocator.Resolve<VocabNoteRenderer>();
   // ReSharper disable once UnusedMember.Global used from python
   public SentenceNoteRenderer SentenceNoteRenderer => _serviceLocator.Resolve<SentenceNoteRenderer>();
   // ReSharper disable once UnusedMember.Global used from python
   public KanjiNoteRenderer KanjiNoteRenderer => _serviceLocator.Resolve<KanjiNoteRenderer>();
}
