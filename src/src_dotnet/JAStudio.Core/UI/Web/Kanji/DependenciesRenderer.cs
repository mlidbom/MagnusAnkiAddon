using JAStudio.Core.Note;
using JAStudio.Core.SysUtils;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace JAStudio.Core.UI.Web.Kanji;

public static class DependenciesRenderer
{
    public static string RenderDependenciesList(KanjiNote note)
    {
        var readings = note.GetReadingsClean();

        string HighlightPrimaryReadingSources(string text)
        {
            foreach (var reading in readings)
            {
                var hiragana = KanaUtils.KatakanaToHiragana(reading);
                var katakana = KanaUtils.HiraganaToKatakana(reading);
                
                text = Regex.Replace(text, $@"\b{Regex.Escape(hiragana)}\b", 
                    $"<primary-reading-source>{hiragana}</primary-reading-source>");
                text = Regex.Replace(text, $@"\b{Regex.Escape(katakana)}\b", 
                    $"<primary-reading-source>{katakana}</primary-reading-source>");
            }
            return text;
        }

        var dependencies = note.GetRadicalsNotes();

        string FormatReadings(KanjiNote kanji)
        {
            var separator = """<span class="readingsSeparator">|</span>""";
            var readingsOn = string.Join(", ", kanji.GetReadingOnListHtml().Select(KanaUtils.HiraganaToKatakana));
            var readingsKun = string.Join(", ", kanji.GetReadingKunListHtml());
            return $"{readingsOn} {separator} {readingsKun}";
        }

        if (dependencies.Count > 0)
        {
            var dependencyItems = dependencies.Select(kanji => $$$"""
    <div class="dependency {{{string.Join(" ", kanji.GetMetaTags())}}}">
        <div class="dependency_heading">
            <div class="dependency_character clipboard">{{{kanji.GetQuestion()}}}</div>
            <div class="dependency_name clipboard">{{{kanji.GetAnswer()}}}</div>
            <div class="dependency_readings">{{{HighlightPrimaryReadingSources(FormatReadings(kanji))}}}</div>
        </div>
        <div class="dependency_mnemonic">{{{kanji.GetActiveMnemonic()}}}</div>
    </div>
""");

            return $"""
                <div id="dependencies_list" class="page_section">
                    <div class="page_section_title">radicals</div>
                {string.Join("\n", dependencyItems)}
                </div>
                """;
        }

        return "";
    }
}
