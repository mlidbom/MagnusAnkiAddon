using JAStudio.Core.Configuration;
using JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;
using JAStudio.Core.Note;
using JAStudio.Core.UI.Web.Sentence;
using JAStudio.Core.ViewModels.KanjiList;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace JAStudio.Core.UI.Web.Sentence;

public static class UdSentenceBreakdownRenderer
{
    private static string FormatReason(string reason)
    {
        return reason.Contains("configured") 
            ? $"""<span class="configured">{reason}</span>""" 
            : reason;
    }

    private static string BuildInvalidForDisplaySpan(MatchViewModel viewModel)
    {
        if (!Settings.ShowBreakdownInEditMode() || 
            (viewModel.IncorrectReasons.Count == 0 && viewModel.HidingReasons.Count == 0))
            return "";

        var incorrectReasons = viewModel.IncorrectReasons
            .Select(reason => $"""<div class="incorrect_reason">{FormatReason(reason)}</div>""");
        var hidingReasons = viewModel.HidingReasons
            .Select(reason => $"""<div class="hiding_reason">{FormatReason(reason)}</div>""");

        return $"""<span>{string.Join("\n", incorrectReasons.Concat(hidingReasons))}</span>""";
    }

    private static string RenderMatchKanji(MatchViewModel match)
    {
        if (!match.ShowKanji)
            return "";

        var viewmodel = SentenceKanjiListViewModel.Create(match.Kanji);

        var kanjiItems = viewmodel.KanjiList.Select(kanji =>
        {
            var mnemonicHtml = match.ShowKanjiMnemonics 
                ? $"""<div class="kanji_mnemonic">{kanji.Mnemonic()}</div>""" 
                : "";

            return $$$"""
    <div class="kanji_item {{{string.Join(" ", kanji.Kanji.GetMetaTags())}}}">
        <div class="kanji_main">
            <span class="kanji_kanji clipboard">{{{kanji.Question()}}}</span>
            <span class="kanji_answer">{{{kanji.Answer()}}}</span>
            <span class="kanji_readings">{{{kanji.Readings()}}}</span>
        </div>
        {{{mnemonicHtml}}}
    </div>
""";
        });

        return $"""
            <div class="vocab_kanji_list">
            {string.Join("\n", kanjiItems)}
            </div>
            """;
    }

    private static readonly Dictionary<string, string> ToggleAbbreviations = new()
    {
        { "show_sentence_breakdown_in_edit_mode", "EM" },
        { "show_kanji_in_sentence_breakdown", "SK" },
        { "show_compound_parts_in_sentence_breakdown", "SCP" },
        { "show_kanji_mnemonics_in_sentence_breakdown", "SKM" },
        { "automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound", "YSV" },
        { "automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound", "YPV" },
        { "automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound", "YCV" },
        { "hide_compositionally_transparent_compounds", "HCTC" },
        { "hide_all_compounds", "HAC" }
    };

    private static string GetToggleAbbreviation(string toggle)
    {
        return ToggleAbbreviations.TryGetValue(toggle, out var abbr) 
            ? abbr 
            : $"MISSING_ABBREVIATION:{toggle}";
    }

    private static string RenderToggle(ConfigurationValue<bool> toggle)
    {
        return $"""<span class="toggle {toggle.Name}" title="{toggle.Title}">{GetToggleAbbreviation(toggle.Name)}</span>  """;
    }

    private static string RenderToggleList()
    {
        return string.Join("\n", 
            App.Config().SentenceViewToggles
                .Where(toggle => toggle.GetValue())
                .Select(RenderToggle));
    }

    private static string RenderViewSettings()
    {
        return $"""
            <span class="view_settings">
                <span class="view_settings_title">Settings:</span>
                {RenderToggleList()}
            </span>
            """;
    }

    public static string RenderSentenceAnalysis(SentenceNote note)
    {
        var sentenceAnalysis = new SentenceViewModel(note);
        var html = new StringBuilder();

        html.AppendLine($"""
            <div class="breakdown page_section">
                <div class="page_section_title">Sentence breakdown  #  {RenderViewSettings()}</div>
                <ul class="sentenceVocabList userExtra depth1">
            """);

        foreach (var match in sentenceAnalysis.DisplayedMatches)
        {
            var vocabFormHtml = match.DisplayVocabForm 
                ? $"""<span class="vocabHitForm clipboard">{match.VocabForm}</span>""" 
                : "";
            var readingsHtml = match.DisplayReadings 
                ? $"""<span class="vocabHitReadings clipboard">{match.Readings}</span>""" 
                : "";

            html.AppendLine($$$"""
                    <li class="sentenceVocabEntry depth1 word_priority_very_high {{{match.MetaTagsString}}}">
                        <div class="sentenceVocabEntryDiv">
                            {{{BuildInvalidForDisplaySpan(match)}}}
                            <audio src="{{{match.AudioPath}}}"></audio><a class="play-button"></a>
                            <span class="vocabQuestion clipboard">{{{match.ParsedForm}}}</span>
                            {{{vocabFormHtml}}}
                            {{{readingsHtml}}}
                            {{{match.MetaTagsHtml}}}
                            <span class="vocabAnswer">{{{match.Answer}}}</span>
                        </div>
                    </li>
                    """);

            if (match.ShowCompoundParts)
            {
                foreach (var compoundPart in match.CompoundParts)
                {
                    var compoundReadingsHtml = compoundPart.DisplayReadings 
                        ? $"""<span class="vocabHitReadings clipboard">{compoundPart.Readings}</span>""" 
                        : "";

                    html.AppendLine($$$"""
                            <li class="sentenceVocabEntry compound_part {{{compoundPart.MetaTagsString}}}">
                                <div class="sentenceVocabEntryDiv">
                                    <audio src="{{{compoundPart.AudioPath}}}"></audio><a class="play-button"></a>
                                    <span class="vocabQuestion clipboard">{{{compoundPart.Question}}}</span>
                                    {{{compoundReadingsHtml}}}
                                    {{{compoundPart.MetaTagsHtml}}}
                                    <span class="vocabAnswer">{{{compoundPart.Answer}}}</span>
                                </div>
                            </li>
                        """);
                }
            }

            html.AppendLine($$$"""
        <li class="sentenceVocabEntry depth1 word_priority_very_high {{{match.MetaTagsString}}}">
            {{{RenderMatchKanji(match)}}}
        </li>
""");
        }

        html.AppendLine("""
            </ul>
            </div>
            """);

        html.Append(RenderTokens(sentenceAnalysis));

        return html.ToString();
    }

    private static readonly List<(Func<IAnalysisToken, bool> Predicate, string Abbr, string Title)> TokenBooleanFlags = new()
    {
        (t => t.IsPastTenseStem, "PTS", "past_tense_stem"),
        (t => t.IsPastTenseMarker, "PTM", "past_tense_marker"),
        (t => t.IsMasuStem, "Masu", "masu_stem"),
        (t => t.IsAdverb, "Adv", "adverb"),
        (t => t.IsIrrealis, "Irr", "irrealis"),
        (t => t.IsEndOfStatement, "EOS", "end_of_statement"),
        (t => t.HasTeFormStem, "HTFS", "has_te_form_stem"),
        (t => t.IsNonWordCharacter, "NWC", "non_word_character"),
        (t => t.IsDictionaryVerbFormStem, "DVS", "dictionary_verb_form_stem"),
        (t => t.IsDictionaryVerbInflection, "DVI", "dictionary_verb_inflection"),
        (t => t.IsGodanPotentialStem, "GPS", "godan_potential_stem"),
        (t => t.IsGodanImperativeStem, "GIS", "godan_imperative_stem"),
        (t => t.IsIchidanImperativeStem, "IIS", "ichidan_imperative_stem"),
        (t => t.IsGodanPotentialInflection, "GPI", "godan_potential_inflection"),
        (t => t.IsGodanImperativeInflection, "GII", "godan_imperative_inflection"),
        (t => t.IsIchidanImperativeInflection, "III", "ichidan_imperative_inflection"),
        (t => t.IsInflectableWord, "Infl", "inflectable_word"),
        (t => t.IsIchidanVerb, "一段", "ichidan_verb"),
        (t => t.IsGodanVerb, "五弾", "godan_verb"),
    };

    private static string RenderTokens(SentenceViewModel sentenceAnalysis)
    {
        if (!Settings.ShowBreakdownInEditMode())
            return "";

        var tokens = sentenceAnalysis.Analysis.Analysis.PreProcessedTokens.ToList();
        var html = RenderTokenList(tokens, "Tokens");

        if (tokens.Any(it => it is not JNToken))
        {
            html += RenderTokenList(sentenceAnalysis.Analysis.Analysis.TokenizedText.Tokens.Cast<IAnalysisToken>().ToList(), "Unprocessed Tokens");
        }

        return html;
    }

    private static string RenderTokenProperties(IAnalysisToken token)
    {
        var properties = TokenBooleanFlags
            .Where(flag => flag.Predicate(token))
            .Select(flag => $"""<span class="token_property" title="{flag.Title}">{flag.Title}</span>""")
            .ToList();

        return properties.Count > 0 ? string.Join(", ", properties) : "";
    }

    private static string RenderTokenList(List<IAnalysisToken> tokens, string sectionTitle)
    {
        var html = new StringBuilder();

        html.AppendLine($"""
            <div class="tokens page_section">
                <div class="page_section_title">{sectionTitle}</div>
                <table>
                    <thead>
                        <tr>
                            <th>Surface</th>
                            <th>Base</th>
                            <th>Boolean flags</th>
                            <th>Token class</th>
                            <th title="Parts of speech">POS1</th>
                            <th title="Parts of speech">POS2</th>
                            <th title="Parts of speech">POS3</th>
                            <th title="Parts of speech">POS4</th>
                            <th title="Inflected form">Inflected Form</th>
                            <th title="Inflection type">Inflection Type</th>
                        </tr>
                    </thead>
                    <tbody>
            """);

        foreach (var token in tokens)
        {
            var customTokenClass = token is not JNToken ? "custom_token_class" : "";
            
            html.AppendLine($$$"""
                    <tr>
                        <td class="surface"><span class="japanese clipboard">{{{token.Surface}}}</span></td>
                        <td class="base"><span class="japanese clipboard">{{{token.BaseForm}}}</span></td>
                        <td class="token_properties">{{{RenderTokenProperties(token)}}}</td>
                        <td class="token_properties {{{customTokenClass}}}">{{{token.GetType().Name}}}</td>
                        <td class="pos pos1"><span class="japanese clipboard">{{{token.SourceToken.PartsOfSpeech.Level1.Japanese}}}</span>:{{{token.SourceToken.PartsOfSpeech.Level1.English}}}</td>
                        <td class="pos pos2"><span class="japanese clipboard">{{{token.SourceToken.PartsOfSpeech.Level2.Japanese}}}</span>:{{{token.SourceToken.PartsOfSpeech.Level2.English}}}</td>
                        <td class="pos pos3"><span class="japanese clipboard">{{{token.SourceToken.PartsOfSpeech.Level3.Japanese}}}</span>:{{{token.SourceToken.PartsOfSpeech.Level3.English}}}</td>
                        <td class="pos pos4"><span class="japanese clipboard">{{{token.SourceToken.PartsOfSpeech.Level4.Japanese}}}</span>:{{{token.SourceToken.PartsOfSpeech.Level4.English}}}</td>
                        <td class="inflected_form clipboard">{{{token.SourceToken.InflectedForm}}}</td>
                        <td class="inflection_type clipboard">{{{token.SourceToken.InflectionType}}}</td>
                    </tr>
                """);
        }

        html.AppendLine("""
                    </tbody>
                </table>
            </div>
            """);

        return html.ToString();
    }
}
