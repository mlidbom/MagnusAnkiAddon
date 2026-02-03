using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace JAStudio.Core;

public static class StringExtensions
{
    private static readonly Regex HtmlTagRegex = new(@"<[^>]*>", RegexOptions.Compiled);

    public static string StripHtmlMarkup(string input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return string.Empty;
        }

        return HtmlTagRegex.Replace(input, string.Empty);
    }

    public static List<string> ExtractCommaSeparatedValues(string input)
    {
        if (string.IsNullOrWhiteSpace(input))
        {
            return new List<string>();
        }

        return input.Split(',')
            .Select(s => s.Trim())
            .Where(s => !string.IsNullOrEmpty(s))
            .ToList();
    }

    public static string ReplaceWord(string word, string replacement, string text)
    {
        if (string.IsNullOrEmpty(text))
        {
            return text;
        }

        // Simple word replacement - can be enhanced with word boundary detection
        return text.Replace(word, replacement);
    }

    public static string FirstNumber(string input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return string.Empty;
        }

        var match = Regex.Match(input, @"\d+");
        return match.Success ? match.Value : string.Empty;
    }

    public const string InvisibleSpace = "\u200B"; // Zero-width space
}
