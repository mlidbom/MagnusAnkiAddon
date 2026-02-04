using System.Linq;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.Note.Vocabulary;

public static class VocabNoteGeneratedData
{
    public static void UpdateGeneratedData(VocabNote vocab)
    {
        vocab.MetaData.SentenceCount.Set(vocab.Sentences.All().Count);
        vocab.SetField(NoteFieldsConstants.Vocab.ActiveAnswer, vocab.GetAnswer());
        
        // TODO: Implement when perfect_synonyms is ported
        // vocab.RelatedNotes.PerfectSynonyms.PushAnswerToOtherSynonyms();

        var question = vocab.Question.WithoutNoiseCharacters.Trim();
        var readings = string.Join(",", vocab.GetReadings());

        if (string.IsNullOrEmpty(readings) && KanaUtils.IsOnlyKana(question))
        {
            vocab.SetReadings(new System.Collections.Generic.List<string> { question });
            vocab.Tags.Set(Tags.Vocab.UsuallyKanaOnly);
        }

        if (vocab.CompoundParts.All().Count == 0 && vocab.PartsOfSpeech.IsSuruVerbIncluded())
        {
            var compounds = new[] { question.Substring(0, question.Length - 2), "する" }.ToList();
            vocab.CompoundParts.Set(compounds);
        }

        if (!string.IsNullOrEmpty(vocab.GetQuestion()))
        {
            // TODO: Implement dictionary lookup and form generation when DictLookup is ported
            // var speechTypes = vocab.PartsOfSpeech.Get().Except(new[] { POS.Unknown, "Godan verbIchidan verb", "Ichidan verbGodan verb" });
            
            // if (vocab.GetReadings().Any())
            // {
            //     var lookup = DictLookup.LookupVocabWordOrName(vocab);
            //     if (lookup.IsUk() && !vocab.Tags.Contains(Tags.DisableKanaOnly))
            //     {
            //         vocab.Tags.Set(Tags.UsuallyKanaOnly);
            //     }
            //     
            //     if (!vocab.Forms.AllSet().Any())
            //     {
            //         if (lookup.FoundWords())
            //         {
            //             vocab.Forms.SetSet(lookup.ValidForms(vocab.PartsOfSpeech.IsUk()));
            //         }
            //         
            //         if (vocab.PartsOfSpeech.IsUk() && !vocab.Forms.AllSet().Contains(vocab.GetReadings()[0]))
            //         {
            //             vocab.Forms.SetSet(vocab.Forms.AllSet().Union(vocab.GetReadings()).ToHashSet());
            //         }
            //     }
            //     
            //     if (speechTypes.Count() == 0)
            //     {
            //         vocab.PartsOfSpeech.SetAutomaticallyFromDictionary();
            //     }
            // }

            if (!vocab.Forms.AllSet().Contains(vocab.GetQuestion()) && vocab.Question.IsValid)
            {
                var updatedForms = vocab.Forms.AllSet().Union(new[] { vocab.GetQuestion() }).ToHashSet();
                vocab.Forms.SetSet(updatedForms);
            }
        }
    }
}
