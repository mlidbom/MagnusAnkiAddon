using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.ViewModels.KanjiList;

public class KanjiListViewModel
{
   public List<KanjiViewModel> KanjiList { get; }

   public KanjiListViewModel(List<KanjiViewModel> kanjiList) => KanjiList = kanjiList;

   public override string ToString()
   {
      return string.Join("\n", KanjiList.Select(kan => kan.ToString()));
   }
}
