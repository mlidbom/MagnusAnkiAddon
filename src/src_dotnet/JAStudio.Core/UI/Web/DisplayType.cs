using System.Collections.Generic;

namespace JAStudio.Core.UI.Web;

/// <summary>
/// Display type constants and checks.
/// </summary>
public static class DisplayType
{
    public const string ReviewQuestion = "reviewQuestion";
    public const string ReviewAnswer = "reviewAnswer";

    private static readonly HashSet<string> AnswerTypes = ["reviewAnswer", "previewAnswer", "clayoutAnswer"];

    public static bool IsDisplayingAnswer(string displayType) => AnswerTypes.Contains(displayType);

    public static bool IsDisplayingReviewQuestion(string displayType) => displayType == ReviewQuestion;

    public static bool IsDisplayingReviewAnswer(string displayType) => displayType == ReviewAnswer;
}
