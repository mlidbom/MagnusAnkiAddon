using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.Note;

public abstract class JPNote
{
   public NoteFlushGuard RecursiveFlushGuard { get; }
   int _hashValue;

   readonly HashSet<string> _unsuspendedCards = new();
   public NoteTags Tags { get; }

   readonly Dictionary<string, string> _fields;
   int _idCache;

   protected JPNote(JPNoteData? data = null)
   {
      RecursiveFlushGuard = new NoteFlushGuard(this);
      _hashValue = 0;

      Tags = new NoteTags(this, data);

      _fields = data?.Fields ?? new Dictionary<string, string>();
      _idCache = data?.Id ?? 0;
   }

   public bool IsFlushing => RecursiveFlushGuard.IsFlushing;

   public void SetStudyingStatus(CardStudyingStatus status)
   {
      if(_unsuspendedCards.Contains(status.CardType))
      {
         if(status.IsSuspended)
         {
            _unsuspendedCards.Remove(status.CardType);
         }
      } else
      {
         if(!status.IsSuspended)
         {
            _unsuspendedCards.Add(status.CardType);
         }
      }
   }

   public JPNoteData GetData() => new(GetId(), _fields, Tags.ToInternedStringList());

   public override bool Equals(object? obj)
   {
      var id = GetId();
      if(id == 0)
      {
         throw new InvalidOperationException("You cannot compare or hash a note that has not been saved yet since it has no id");
      }

      return obj is JPNote other && other.GetId() == id;
   }

   public abstract void UpdateInCache();

   public bool IsStudying(string? cardType = null)
   {
      if(cardType == null)
      {
         return _unsuspendedCards.Count > 0;
      }

      return _unsuspendedCards.Contains(cardType);
   }

   public bool IsStudyingRead() => IsStudying(CardTypes.Reading);
   public bool IsStudyingListening() => IsStudying(CardTypes.Listening);

   public void SuspendAllCards() => throw new NotImplementedException();

   public void UnsuspendAllCards() => throw new NotImplementedException();

   public bool HasSuspendedCards() => throw new NotImplementedException();

   public bool HasActiveCards() => IsStudying();

   public override int GetHashCode()
   {
      if(_hashValue == 0)
      {
         _hashValue = GetId();
         if(_hashValue == 0)
         {
            throw new InvalidOperationException("You cannot compare or hash a note that has not been saved yet since it has no id");
         }
      }

      return _hashValue;
   }

   public override string ToString() => $"{GetQuestion()}: {GetAnswer()}";

   public JPCollection Collection => App.Col();

   public virtual string GetQuestion()
   {
      var value = GetField(MyNoteFields.Question);
      return !string.IsNullOrEmpty(value) ? value : "[EMPTY]";
   }

   public virtual string GetAnswer() => GetField(MyNoteFields.Answer);

   public virtual HashSet<JPNote> GetDirectDependencies() => new();

   public virtual void OnTagsUpdated()
   {
      // Called when tags are modified. Subclasses can override to invalidate cached state.
   }

   HashSet<JPNote> GetDependenciesRecursive(HashSet<JPNote> found)
   {
      if(found.Contains(this))
      {
         return found;
      }

      found.Add(this);

      foreach(var dependency in GetDirectDependencies())
      {
         dependency.GetDependenciesRecursive(found);
      }

      return found;
   }

   public HashSet<JPNote> GetDependenciesRecursive() => GetDependenciesRecursive(new HashSet<JPNote>());

   public int GetId() => _idCache;

   public void SetId(int id)
   {
      if(_idCache != 0)
      {
         throw new InvalidOperationException("Cannot change id of a note that has already been saved");
      }

      _idCache = id;
   }

   public virtual void UpdateGeneratedData()
   {
      // Override in subclasses
   }

   public string GetField(string fieldName) => _fields.TryGetValue(fieldName, out var value) ? value : string.Empty;

   bool IsPersisted() => _idCache != 0;

   public void Flush()
   {
      if(IsPersisted())
      {
         RecursiveFlushGuard.Flush();
      }
   }

   public void SetField(string fieldName, string value)
   {
      var fieldValue = GetField(fieldName);
      if(fieldValue != value)
      {
         _fields[fieldName] = value;
         Flush();
      }
   }

   public int PriorityTagValue()
   {
      foreach(var tag in Tags)
      {
         if(tag.Name.StartsWith(Note.Tags.PriorityFolder))
         {
            var numberStr = StringExtensions.FirstNumber(tag.Name);
            if(int.TryParse(numberStr, out var num))
            {
               return num;
            }
         }
      }

      return 0;
   }

   public HashSet<string> GetMetaTags()
   {
      var tags = new HashSet<string>();

      foreach(var tag in Tags)
      {
         if(tag.Name.StartsWith(Note.Tags.PriorityFolder))
         {
            if(tag.Name.Contains("high")) tags.Add("high_priority");
            if(tag.Name.Contains("low")) tags.Add("low_priority");
         }
      }

      if(IsStudying(CardTypes.Reading) || IsStudying(CardTypes.Listening))
      {
         tags.Add("is_studying");
      }

      if(IsStudying(CardTypes.Reading)) tags.Add("is_studying_reading");
      if(IsStudying(CardTypes.Listening)) tags.Add("is_studying_listening");
      if(Tags.Contains(Note.Tags.TTSAudio)) tags.Add("tts_audio");

      return tags;
   }

   public string GetSourceTag()
   {
      var sourceTags = Tags.Where(t => t.Name.StartsWith(Note.Tags.Source.Folder)).ToList();
      if(sourceTags.Any())
      {
         var sorted = sourceTags.OrderBy(t => t.Name.Length).ToList();
         return sorted[0].Name.Substring(Note.Tags.Source.Folder.Length);
      }

      return string.Empty;
   }
}
