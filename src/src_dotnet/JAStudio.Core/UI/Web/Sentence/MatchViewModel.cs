using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.SysUtils;
using Settings = JAStudio.Core.Configuration.Settings;

namespace JAStudio.Core.UI.Web.Sentence;

public class MatchViewModel
{
    private readonly SentenceConfiguration _config;
    private readonly List<string> _metaTags;

    public Match Match { get; }
    public bool MatchIsDisplayed { get; }
    public VocabMatch? VocabMatch { get; }
    public CandidateWordVariantViewModel WordVariantVm { get; }
    public bool IsDisplayWord { get; }
    public string ParsedForm { get; }
    public string Answer { get; }
    public string VocabForm { get; }
    public List<CompoundPartViewModel> CompoundParts { get; }
    public string AudioPath { get; }
    public bool IsHighlighted { get; }
    public string Readings { get; }
    public string MetaTagsHtml { get; }
    public bool DisplayVocabForm { get; }
    public bool MatchOwnsForm { get; }
    public bool DisplayReadings { get; }

    public MatchViewModel(CandidateWordVariantViewModel wordVariantVm, Match match)
    {
        Match = match;
        MatchIsDisplayed = match.IsDisplayed;
        VocabMatch = match as VocabMatch;
        _config = wordVariantVm.CandidateWord.Word.Analysis.Configuration;
        WordVariantVm = wordVariantVm;
        IsDisplayWord = wordVariantVm.IsDisplayWord;
        ParsedForm = match.ParsedForm;
        Answer = match.Answer;
        VocabForm = !Settings.ShowBreakdownInEditMode() ? match.MatchForm : match.ExclusionForm;
        CompoundParts = new List<CompoundPartViewModel>();
        AudioPath = string.Empty;
        IsHighlighted = _config.HighlightedWords.Contains(ParsedForm) || _config.HighlightedWords.Contains(VocabForm);
        Readings = string.Join(", ", match.Readings);
        MetaTagsHtml = string.Empty;
        _metaTags = new List<string>();
        DisplayVocabForm = ParsedForm != VocabForm;
        MatchOwnsForm = ParsedForm == VocabForm;
        DisplayReadings = ParsedForm != Readings;

        if (VocabMatch != null)
        {
            CompoundParts = CompoundPartViewModel.GetCompoundPartsRecursive(this, VocabMatch.Vocab, _config);
            AudioPath = VocabMatch.Vocab.Audio.GetPrimaryAudioPath();
            _metaTags = VocabMatch.Vocab.GetMetaTags().ToList();
            MetaTagsHtml = VocabMatch.Vocab.MetaData.MetaTagsHtml(displayExtendedSentenceStatistics: false);
            MatchOwnsForm = VocabMatch.Vocab.Forms.IsOwnedForm(ParsedForm);
            if (ParsedForm != VocabForm)
            {
                DisplayVocabForm = true;
                DisplayReadings = DisplayReadings && VocabForm != Readings;
            }
        }
    }

    public string MetaTagsString => string.Join(" ", MetaTagsList);

    public List<string> MetaTagsList
    {
        get
        {
            var result = new List<string>(_metaTags);
            if (IsHighlighted) result.Add("highlighted");
            result.AddRange(HidingReasons);
            return result;
        }
    }

    public List<string> IncorrectReasons => Match.FailureReasons.ToList();

    public List<string> HidingReasons => Match.HidingReasons.ToList();

    public bool IsDisplayed
    {
        get
        {
            if (Settings.ShowBreakdownInEditMode()) return true;
            return IsDisplayWord && Match.IsDisplayed;
        }
    }

    public bool ShowKanji => Kanji.Any() && !Settings.ShowBreakdownInEditMode() && Settings.ShowKanjiInSentenceBreakdown();

    public bool ShowKanjiMnemonics => Settings.ShowKanjiMnemonicsInSentenceBreakdown();

    public bool ShowCompoundParts => CompoundParts.Any() && !Settings.ShowBreakdownInEditMode();

    public List<string> Kanji
    {
        get
        {
            var kanjiChars = KanaUtils.ExtractKanji(ParsedForm + VocabForm);
            return kanjiChars.Distinct().ToList();
        }
    }

    public override string ToString()
    {
        var flags = new List<string> { ParsedForm };
        if (IsDisplayWord) flags.Add("is_display_word");
        if (IsDisplayed) flags.Add("displayed");
        return string.Join(" ", flags);
    }
}
