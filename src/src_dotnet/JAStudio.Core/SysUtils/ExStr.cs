using System.Text.RegularExpressions;

namespace JAStudio.Core.SysUtils;

public static partial class ExStr
{
   // Pattern: HTML tags, bracket markup, and noise character 〜
   [GeneratedRegex(@"<.*?>|\[.*?\]|[〜]")]
   private static partial Regex HtmlBracketNoisePattern();

   public static string StripHtmlAndBracketMarkupAndNoiseCharacters(string input) => HtmlBracketNoisePattern().Replace(input, "");
}
