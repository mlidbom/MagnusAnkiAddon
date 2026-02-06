using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteGeneratedData
{
   readonly TemporaryServiceCollection _services;
   internal VocabNoteGeneratedData(TemporaryServiceCollection services) => _services = services;

    public static void UpdateGeneratedData(VocabNote vocab)
    {
        vocab.MetaData.SentenceCount.Set(vocab.Sentences.All().Count);
        vocab.SetField(NoteFieldsConstants.Vocab.ActiveAnswer, vocab.GetAnswer());
        vocab.RelatedNotes.PerfectSynonyms.PushAnswerToOtherSynonyms();

        var question = vocab.Question.WithoutNoiseCharacters.Trim();
        var readings = string.Join(",", vocab.GetReadings());

        if (string.IsNullOrEmpty(readings) && KanaUtils.IsOnlyKana(question))
        {
            vocab.SetReadings(new List<string> { question });
            vocab.Tags.Set(Tags.Vocab.UsuallyKanaOnly);
        }

        if (vocab.CompoundParts.All().Count == 0 && vocab.PartsOfSpeech.IsSuruVerbIncluded())
        {
            var compounds = new List<string> { question.Substring(0, question.Length - 2), "する" };
            vocab.CompoundParts.Set(compounds);
        }

        if (!string.IsNullOrEmpty(vocab.GetQuestion()))
        {
            var excludedPOS = new HashSet<string> { POS.Unknown, "Godan verbIchidan verb", "Ichidan verbGodan verb" };
            var speechTypes = vocab.PartsOfSpeech.Get().Except(excludedPOS).ToHashSet();

            if (vocab.GetReadings().Any())
            {
                var lookup = DictLookup.LookupVocabWordOrName(vocab);
                if (lookup.IsUk() && !vocab.Tags.Contains(Tags.DisableKanaOnly))
                {
                    vocab.Tags.Set(Tags.Vocab.UsuallyKanaOnly);
                }

                if (!vocab.Forms.AllSet().Any())
                {
                    if (lookup.FoundWords())
                    {
                        vocab.Forms.SetSet(lookup.ValidForms(vocab.PartsOfSpeech.IsUk()));
                    }

                    if (vocab.PartsOfSpeech.IsUk() && !vocab.Forms.AllSet().Contains(vocab.GetReadings()[0]))
                    {
                        vocab.Forms.SetSet(vocab.Forms.AllSet().Union(vocab.GetReadings()).ToHashSet());
                    }
                }

                if (!speechTypes.Any())
                {
                    vocab.PartsOfSpeech.SetAutomaticallyFromDictionary();
                }
            }

            if (!vocab.Forms.AllSet().Contains(vocab.GetQuestion()) && vocab.Question.IsValid)
            {
                var updatedForms = vocab.Forms.AllSet().Union(new[] { vocab.GetQuestion() }).ToHashSet();
                vocab.Forms.SetSet(updatedForms);
            }
        }
    }
}
