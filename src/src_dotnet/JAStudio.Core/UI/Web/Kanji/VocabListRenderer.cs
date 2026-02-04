using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.UI.Web.Kanji;

public static class VocabListRenderer
{
    public static string GenerateVocabHtmlList(KanjiNote kanjiNote)
    {
        var primaryVocab = kanjiNote.GetPrimaryVocabsOrDefaults();
        var hasRealPrimaryVocabs = kanjiNote.GetPrimaryVocab().Count > 0;

        string CreateClasses(KanjiNote kanji, VocabNote vocab)
        {
            var classes = string.Join(" ", vocab.GetMetaTags());

            var vocabReadings = vocab.Readings.Get();
            if (primaryVocab.Contains(vocab.GetQuestion()) || 
                (vocabReadings.Count > 0 && kanji.GetPrimaryVocab().Contains(vocabReadings[0])))
            {
                classes += hasRealPrimaryVocabs ? " primary_vocab" : " default_primary_vocab";
            }

            if (!vocab.GetQuestion().Contains(kanjiNote.GetQuestion()))
            {
                classes += " not_matching_kanji";
            }

            return classes;
        }

        var vocabs = kanjiNote.GetVocabNotesSorted();

        if (vocabs.Count > 0)
        {
            var vocabEntries = vocabs.Select(vocabNote =>
            {
                var readings = string.Join(", ", kanjiNote.TagVocabReadings(vocabNote));
                return $$$"""
                    <div class="kanjiVocabEntry {{{CreateClasses(kanjiNote, vocabNote)}}}">
                        <audio src="{{{vocabNote.Audio.GetPrimaryAudioPath()}}}"></audio><a class="play-button"></a>
                        <span class="kanji clipboard">{{{vocabNote.GetQuestion()}}}</span>
                        (<span class="clipboard vocabReading">{{{readings}}}</span>)
                        {{{vocabNote.MetaData.MetaTagsHtml(true)}}}
                        <span class="meaning"> {{{vocabNote.GetAnswer()}}}</span>
                    </div>
""";
            });

            return $"""
                <div class="kanjiVocabList page_section">
                    <div class="page_section_title">vocabulary</div>
                    <div>

                    {string.Join("\n", vocabEntries)}

                    </div>
                </div>
                """;
        }
        
        return "";
    }
}
