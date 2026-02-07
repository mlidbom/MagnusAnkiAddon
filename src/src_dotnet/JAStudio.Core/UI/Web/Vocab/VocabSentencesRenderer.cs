using JAStudio.Core.Note;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.UI.Web.Vocab;

public static class VocabSentencesRenderer
{
    public static string GenerateMarkedInvalidInListHtml(VocabNote vocabNote)
    {
        var allInvalid = vocabNote.Sentences.InvalidIn();
        var shownSentences = allInvalid.Take(30).ToList();

        var sentenceEntries = shownSentences.Select(sentence => $$$"""
                        <div class="highlightedSentenceDiv">
                            <audio src="{{{sentence.Audio.FirstAudioFilePath()}}}"></audio><a class="play-button"></a>
                            <div class="highlightedSentence">
                                <div class="sentenceQuestion"><span class="clipboard">{{{sentence.Question.WithoutInvisibleSpace()}}}</span></div>
                                <div class="sentenceAnswer"> {{{sentence.GetAnswer()}}}</span></div>
                            </div>
                        </div>
                        """);

        var showingMessage = allInvalid.Count > 30 ? " showing first 30" : "";

        return shownSentences.Count > 0 ? $$$"""
             <div id="invalidInSentencesSection" class="page_section invalid_in_sentences">
                <div class="page_section_title" title="primary form hits: ">Marked as invalid in {{{allInvalid.Count}}} sentences{{{showingMessage}}}</span></div>
                <div id="highlightedSentencesList">
                    <div>
                        {{{string.Join("\n", sentenceEntries)}}}
                    </div>
                </div>
            </div>q
            """ : "";
    }

    public static string GenerateValidInListHtml(VocabNote vocabNote)
    {
        var studyingSentences = vocabNote.Sentences.Studying().ToHashSet();

        List<VocabSentenceViewModel> SortSentences(List<VocabSentenceViewModel> sentences)
        {
            return sentences.OrderBy(s => s.IsHighlighted() ? 0 : 1)
                .ThenBy(s => s.Sentence.IsStudyingRead() ? 0 : 1)
                .ThenBy(s => s.Sentence.IsStudyingListening() ? 0 : 1)
                .ThenBy(s => s.VocabIsDisplayed ? 0 : 1)
                .ThenBy(s => string.IsNullOrEmpty(s.Sentence.GetAnswer()) ? 1 : 0)
                .ThenBy(s => s.Sentence.PriorityTagValue())
                .ThenBy(s => s.Sentence.Tags.Contains(Tags.TTSAudio) ? 1 : 0)
                .ThenBy(s => s.ContainsPrimaryForm() ? 0 : 1)
                .ThenBy(s => s.Sentence.Question.WithoutInvisibleSpace().Length)
                .ToList();
        }

        var sentences = SortSentences(
            vocabNote.Sentences.All()
                .Select(sentenceNote => new VocabSentenceViewModel(vocabNote, sentenceNote))
                .ToList()
        );
        
        var primaryFormMatches = sentences.Count(x => x.ContainsPrimaryForm());
        sentences = sentences.Take(30).ToList();

        var sentenceEntries = sentences.Select(sentence => $$$"""
                        <div class="highlightedSentenceDiv {{{sentence.SentenceClasses()}}}">
                            <audio src="{{{sentence.Sentence.Audio.FirstAudioFilePath()}}}"></audio><a class="play-button"></a>
                            <div class="highlightedSentence">
                                <div class="sentenceQuestion"><span class="clipboard">{{{sentence.FormatSentence()}}}</span> <span class="deck_indicator">{{{sentence.Sentence.GetSourceTag()}}}</div>
                                <div class="sentenceAnswer"> {{{sentence.Sentence.GetAnswer()}}}</span></div>
                            </div>
                        </div>
                        """);

        var noStudyingClass = studyingSentences.Count == 0 ? "no_studying_sentences" : "";

        return sentences.Count > 0 ? $$$"""
             <div id="highlightedSentencesSection" class="page_section {{{noStudyingClass}}}">
                <div class="page_section_title" title="primary form hits: {{{primaryFormMatches}}}">sentences: primary form hits: {{{primaryFormMatches}}}, <span class="studing_sentence_count">studying: {{{studyingSentences.Count}}}</span></div>
                <div id="highlightedSentencesList">
                    <div>
                        {{{string.Join("\n", sentenceEntries)}}}
                    </div>
                </div>
            </div>
            """ : "";
    }
}
