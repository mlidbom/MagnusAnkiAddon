using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using Settings = JAStudio.Core.Configuration.Settings;

namespace JAStudio.Core.UI.Web.Sentence;

public class CompoundPartViewModel
{
    public VocabNote VocabNote { get; }
    public int Depth { get; }
    public string Question { get; }
    public string Answer { get; }
    public string Readings { get; }
    public string AudioPath { get; }
    public string MetaTagsHtml { get; }
    public bool DisplayReadings { get; }
    public bool IsHighlighted { get; }
    public string MetaTagsString { get; }

    public CompoundPartViewModel(VocabNote vocabNote, int depth, SentenceConfiguration config)
    {
        VocabNote = vocabNote;
        Depth = depth;
        Question = vocabNote.GetQuestion();
        Answer = vocabNote.GetAnswer();
        Readings = string.Join(", ", vocabNote.GetReadings());
        AudioPath = vocabNote.Audio.GetPrimaryAudioPath();
        MetaTagsHtml = vocabNote.MetaData.MetaTagsHtml(noSentenceStatistics: true);
        DisplayReadings = Question != Readings;
        IsHighlighted = config.HighlightedWords.Contains(Question);

        MetaTagsString = string.Join(" ", vocabNote.GetMetaTags());
        MetaTagsString += $" depth_{depth}";
        MetaTagsString += IsHighlighted ? " highlighted" : "";
    }

    public static List<CompoundPartViewModel> GetCompoundPartsRecursive(
        MatchViewModel matchViewModel,
        VocabNote vocabNote,
        SentenceConfiguration config,
        int depth = 0,
        HashSet<long>? visited = null)
    {
        if (!Settings.HideAllCompounds())
        {
            if (!Settings.ShowCompoundPartsInSentenceBreakdown()) return new List<CompoundPartViewModel>();
            visited ??= new HashSet<long>();
            if (visited.Contains(vocabNote.GetId())) return new List<CompoundPartViewModel>();

            visited.Add(vocabNote.GetId());

            var result = new List<CompoundPartViewModel>();

            foreach (var part in vocabNote.CompoundParts.PrimaryPartsNotes())
            {
                var wrapper = new CompoundPartViewModel(part, depth, config);
                result.Add(wrapper);
                var nestedParts = GetCompoundPartsRecursive(matchViewModel, part, config, depth + 1, visited);
                result.AddRange(nestedParts);
            }

            return result;
        }

        var match = matchViewModel.Match;
        if (match.Inspector.IsIchidanCoveringGodanPotential)
        {
            var godanBase = match.Word.StartLocation.Token.BaseForm;
            var godanPotentialPartBase = match.Word.EndLocation.Token.BaseForm;
            var godan = App.Col().Vocab.WithFormPreferDisambiguationNameOrExactMatch(godanBase);
            var godanPotential = App.Col().Vocab.WithFormPreferDisambiguationNameOrExactMatch(godanPotentialPartBase);
            if (godan.Any() && godanPotential.Any())
            {
                return new List<CompoundPartViewModel>
                {
                    new CompoundPartViewModel(godan.First(), depth, config),
                    new CompoundPartViewModel(godanPotential.First(), depth, config)
                };
            }
            return new List<CompoundPartViewModel>();
        }

        // We may still have parts if janome tokenizes a word we consider a compound as a single token
        return vocabNote.CompoundParts.PrimaryPartsNotes()
            .Select(part => new CompoundPartViewModel(part, depth, config))
            .ToList();
    }
}
