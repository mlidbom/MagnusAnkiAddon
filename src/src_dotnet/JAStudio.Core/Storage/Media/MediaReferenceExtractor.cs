using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using JAStudio.Core.Note;

namespace JAStudio.Core.Storage.Media;

public enum MediaType
{
   Audio,
   Image
}

public record MediaReference(string FileName, MediaType Type);

public static partial class MediaReferenceExtractor
{
   public static List<MediaReference> ExtractAll(JPNote note)
   {
      var references = new List<MediaReference>();

      switch (note)
      {
         case KanjiNote kanji:
            ExtractKanjiMedia(kanji, references);
            break;
         case VocabNote vocab:
            ExtractVocabMedia(vocab, references);
            break;
         case SentenceNote sentence:
            ExtractSentenceMedia(sentence, references);
            break;
      }

      return references;
   }

   static void ExtractKanjiMedia(KanjiNote kanji, List<MediaReference> refs)
   {
      AddAudioReferences(kanji.Audio, refs);
      AddImageReferences(kanji.GetField(NoteFieldsConstants.Kanji.Image), refs);
   }

   static void ExtractVocabMedia(VocabNote vocab, List<MediaReference> refs)
   {
      AddAudioReferences(vocab.Audio.First.RawValue(), refs);
      AddAudioReferences(vocab.Audio.Second.RawValue(), refs);
      AddAudioReferences(vocab.Audio.Tts.RawValue(), refs);
      AddImageReferences(vocab.GetField(NoteFieldsConstants.Vocab.Image), refs);
      AddImageReferences(vocab.GetField(NoteFieldsConstants.Vocab.UserImage), refs);
   }

   static void ExtractSentenceMedia(SentenceNote sentence, List<MediaReference> refs)
   {
      foreach (var audioFile in sentence.Audio.AudioFilesPaths())
      {
         if (!string.IsNullOrEmpty(audioFile))
            refs.Add(new MediaReference(audioFile, MediaType.Audio));
      }

      AddImageReferences(sentence.Screenshot.Value, refs);
   }

   static void AddAudioReferences(string rawValue, List<MediaReference> refs)
   {
      if (string.IsNullOrWhiteSpace(rawValue)) return;

      var matches = SoundTagRegex().Matches(rawValue);
      foreach (Match match in matches)
      {
         var fileName = match.Groups[1].Value.Trim();
         if (!string.IsNullOrEmpty(fileName))
            refs.Add(new MediaReference(fileName, MediaType.Audio));
      }
   }

   static void AddImageReferences(string rawValue, List<MediaReference> refs)
   {
      if (string.IsNullOrWhiteSpace(rawValue)) return;

      var matches = ImgSrcRegex().Matches(rawValue);
      foreach (Match match in matches)
      {
         var fileName = match.Groups[1].Value.Trim();
         if (!string.IsNullOrEmpty(fileName))
            refs.Add(new MediaReference(fileName, MediaType.Image));
      }
   }

   [GeneratedRegex(@"\[sound:([^\]]+)\]")]
   private static partial Regex SoundTagRegex();

   [GeneratedRegex(@"<img[^>]+src\s*=\s*[""']([^""']+)[""']", RegexOptions.IgnoreCase)]
   private static partial Regex ImgSrcRegex();
}
