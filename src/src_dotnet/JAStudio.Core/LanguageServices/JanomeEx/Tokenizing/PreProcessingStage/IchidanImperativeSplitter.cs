using System.Collections.Generic;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;

static class IchidanImperativeSplitter
{
   public static List<IAnalysisToken>? TrySplit(JNToken token)
   {
      if(IsIchidanImperative(token))
      {
         return SplitIchidanImperative(token);
      }

      return null;
   }

   static bool IsIchidanImperative(JNToken token) =>
      InflectionForms.ImperativeMeireikei.IchidanForms.Contains(token.InflectedForm);

   static List<IAnalysisToken> SplitIchidanImperative(JNToken token)
   {
      var ichidanSurface = token.Surface[..^1];
      var ichidanImperativePart = token.Surface[^1..];
      return
      [
         new SplitToken(token, ichidanSurface, token.BaseForm, isInflectableWord: true, isIchidanImperativeStem: true),
         new SplitToken(token, ichidanImperativePart, ichidanImperativePart, isInflectableWord: true, isIchidanImperativeInflection: true)
      ];
   }
}
