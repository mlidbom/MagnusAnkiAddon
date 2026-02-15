using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.NoteFields;

public class MutableCommaSeparatedStringsListFieldDeDuplicated : MutableCommaSeparatedStringsListField
{
    public MutableCommaSeparatedStringsListFieldDeDuplicated(CachingMutableStringField field) 
        : base(field)
    {
    }

    public override void Set(List<string> value)
    {
        base.Set(value.Distinct().ToList());
    }
}
