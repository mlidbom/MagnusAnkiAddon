using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Note.Vocabulary.RelatedVocab;

namespace JAStudio.Core.Storage.Converters;

public static class VocabNoteConverter
{
    static readonly VocabNoteMatchingRulesSerializer MatchingRulesSerializer = new();
    static readonly RelatedVocabDataSerializer RelatedVocabSerializer = RelatedVocabData.Serializer();

    public static VocabData ToCorpusData(VocabNote note)
    {
        var matchingRulesJson = note.GetField(NoteFieldsConstants.Vocab.MatchingRules);
        var relatedVocabJson = note.GetField(NoteFieldsConstants.Vocab.RelatedVocab);
        var matchingRulesData = MatchingRulesSerializer.Deserialize(matchingRulesJson);
        var relatedVocabData = RelatedVocabSerializer.Deserialize(relatedVocabJson);

        return new VocabData
        {
            Id = note.GetId().Value,
            Question = note.GetField(NoteFieldsConstants.Vocab.Question),
            SourceAnswer = note.GetField(NoteFieldsConstants.Vocab.SourceAnswer),
            UserAnswer = note.GetField(NoteFieldsConstants.Vocab.UserAnswer),
            ActiveAnswer = note.GetField(NoteFieldsConstants.Vocab.ActiveAnswer),
            UserExplanation = note.GetField(NoteFieldsConstants.Vocab.UserExplanation),
            UserExplanationLong = note.GetField(NoteFieldsConstants.Vocab.UserExplanationLong),
            UserMnemonic = note.GetField(NoteFieldsConstants.Vocab.UserMnemonic),
            UserCompounds = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Vocab.UserCompounds)),
            Readings = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Vocab.Reading)),
            PartsOfSpeech = note.GetField(NoteFieldsConstants.Vocab.PartsOfSpeech),
            SourceMnemonic = note.GetField(NoteFieldsConstants.Vocab.SourceMnemonic),
            SourceReadingMnemonic = note.GetField(NoteFieldsConstants.Vocab.SourceReadingMnemonic),
            AudioB = note.GetField(NoteFieldsConstants.Vocab.AudioB),
            AudioG = note.GetField(NoteFieldsConstants.Vocab.AudioG),
            AudioTTS = note.GetField(NoteFieldsConstants.Vocab.AudioTTS),
            Forms = StringExtensions.ExtractCommaSeparatedValues(note.GetField(NoteFieldsConstants.Vocab.Forms)),
            SentenceCount = int.TryParse(note.GetField(NoteFieldsConstants.Vocab.SentenceCount), out var sc) ? sc : 0,
            MatchingRules = new VocabMatchingRulesSubData
            {
                PrefixIsNot = matchingRulesData.PrefixIsNot.ToList(),
                SuffixIsNot = matchingRulesData.SuffixIsNot.ToList(),
                SurfaceIsNot = matchingRulesData.SurfaceIsNot.ToList(),
                YieldToSurface = matchingRulesData.YieldToSurface.ToList(),
                RequiredPrefix = matchingRulesData.RequiredPrefix.ToList(),
            },
            RelatedVocab = new VocabRelatedSubData
            {
                ErgativeTwin = relatedVocabData.ErgativeTwin,
                DerivedFrom = relatedVocabData.DerivedFrom.Get(),
                PerfectSynonyms = relatedVocabData.PerfectSynonyms.ToList(),
                Synonyms = relatedVocabData.Synonyms.ToList(),
                Antonyms = relatedVocabData.Antonyms.ToList(),
                ConfusedWith = relatedVocabData.ConfusedWith.ToList(),
                SeeAlso = relatedVocabData.SeeAlso.ToList(),
            },
            Tags = note.Tags.ToStringList(),
        };
    }
}
