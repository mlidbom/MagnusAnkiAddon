using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.NoteFields;

public class MutableCommaSeparatedStringsListFieldDeDuplicated : MutableCommaSeparatedStringsListField
{
    public MutableCommaSeparatedStringsListFieldDeDuplicated(JPNote note, string fieldName) 
        : base(note, fieldName)
    {
    }

    public override void Set(List<string> value)
    {
        base.Set(value.Distinct().ToList());
    }
}
