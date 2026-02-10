using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note;

public class NoteTags : IEnumerable<Tag>
{
   readonly JPNote _note;
   readonly HashSet<Tag> _tags = new();

   public NoteTags(JPNote note, NoteData? data = null)
   {
      _note = note;

      if(data != null)
      {
         foreach(var tagName in data.Tags)
         {
            _tags.Add(Tag.FromName(tagName));
         }
      }
   }

   void Persist()
   {
      _note.Flush();
      _note.OnTagsUpdated();
   }

   public bool Contains(Tag value) => _tags.Contains(value);

   public void Set(Tag tag)
   {
      if(!Contains(tag))
      {
         _tags.Add(tag);
         Persist();
      }
   }

   public void Unset(Tag tag)
   {
      if(Contains(tag))
      {
         _tags.Remove(tag);
         Persist();
      }
   }

   public void Toggle(Tag tag, bool on)
   {
      if(on)
      {
         Set(tag);
      } else
      {
         Unset(tag);
      }
   }

   public IEnumerator<Tag> GetEnumerator() => _tags.GetEnumerator();

   IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

   public List<string> ToStringList()
   {
      return this.Select(t => t.Name).OrderBy(n => n).ToList();
   }
}
