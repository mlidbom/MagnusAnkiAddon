namespace JAStudio.Core.Note.Sentences.Serialization;

public class ParsedWordSerializer
{
    public static readonly string Separator = $" {StringExtensions.InvisibleSpace} ";

    public static string ToRow(ParsedMatch parsedWord)
    {
        return string.Join(Separator, new[]
        {
            parsedWord.Variant,
            parsedWord.StartIndex.ToString(),
            parsedWord.IsDisplayed ? "1" : "0",
            parsedWord.ParsedForm,
            parsedWord.VocabId.ToString()
        });
    }

    public static ParsedMatch FromRow(string serialized)
    {
        var values = serialized.Split(new[] { Separator }, System.StringSplitOptions.None);

        return new ParsedMatch(
            values[0],
            int.Parse(values[1]),
            values[2] != "0",
            values[3],
            long.Parse(values[4])
        );
    }
}
