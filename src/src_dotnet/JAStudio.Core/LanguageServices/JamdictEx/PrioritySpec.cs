using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.LanguageServices.JamdictEx;

public class PrioritySpec
{
    private static readonly HashSet<string> FrequencyMaximum;
    private static readonly HashSet<string> FrequencyHigh;
    private static readonly HashSet<string> FrequencyMedium;
    private static readonly HashSet<string> FrequencyLow;

    private static readonly HashSet<string> TagsMaximum = new() { "ichi1" };
    private static readonly HashSet<string> TagsHigh = new() { "news1", "spec1" };
    private static readonly HashSet<string> TagsMedium = new() { "news2", "spec2" };

    static PrioritySpec()
    {
        FrequencyMaximum = Enumerable.Range(1, 9).Select(num => $"nf{num:D2}").ToHashSet();
        FrequencyHigh = Enumerable.Range(11, 9).Select(num => $"nf{num}").ToHashSet();
        FrequencyMedium = Enumerable.Range(21, 19).Select(num => $"nf{num}").ToHashSet();
        FrequencyLow = Enumerable.Range(41, 19).Select(num => $"nf{num}").ToHashSet();
    }

    public HashSet<string> Tags { get; }
    public string PriorityString { get; }
    public int Priority { get; }

    public PrioritySpec(HashSet<string> tags)
    {
        Tags = tags;

        if (tags.Overlaps(TagsMaximum))
        {
            PriorityString = "priority_maximum";
            Priority = 1;
        }
        else if (tags.Overlaps(TagsHigh))
        {
            PriorityString = "priority_high";
            Priority = 11;
        }
        else if (tags.Overlaps(TagsMedium))
        {
            PriorityString = "priority_medium";
            Priority = 21;
        }
        else if (tags.Overlaps(FrequencyMaximum))
        {
            PriorityString = "priority_maximum";
            var tag = tags.Intersect(FrequencyMaximum).First();
            Priority = int.Parse(tag[^1..]);  // the actual number from the nf tag
        }
        else if (tags.Overlaps(FrequencyHigh))
        {
            PriorityString = "priority_high";
            var tag = tags.Intersect(FrequencyHigh).First();
            Priority = int.Parse(tag[^2..]);  // the actual number from the nf tag
        }
        else if (tags.Overlaps(FrequencyMedium))
        {
            PriorityString = "priority_medium";
            var tag = tags.Intersect(FrequencyMedium).First();
            Priority = int.Parse(tag[^2..]);  // the actual number from the nf tag
        }
        else if (tags.Overlaps(FrequencyLow))
        {
            PriorityString = "priority_low";
            var tag = tags.Intersect(FrequencyLow).First();
            Priority = int.Parse(tag[^2..]);  // the actual number from the nf tag
        }
        else
        {
            PriorityString = "priority_low";
            Priority = 50;
        }
    }
}
