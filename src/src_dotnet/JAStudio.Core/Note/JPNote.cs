using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.Note;

public abstract class JPNote
{
   public NoteFlushGuard RecursiveFlushGuard { get; }
   public NoteServices Services { get; }
   int _hashValue;

   // Dictionary tracks card suspend status: true = active/unsuspended, false = suspended
   readonly Dictionary<string, bool> _cardStatus = new();

   public void CopyStudyingStatusFrom(JPNote other)
   {
      foreach(var kvp in other._cardStatus)
      {
         _cardStatus[kvp.Key] = kvp.Value;
      }
   }
   public NoteTags Tags { get; }

   readonly Dictionary<string, string> _fields;
   NoteId _id;

   protected JPNote(NoteServices services, NoteId id, NoteData? data = null)
   {
      Services = services;
      RecursiveFlushGuard = new NoteFlushGuard(this);
      _hashValue = 0;

      Tags = new NoteTags(this, data);

      _fields = data?.Fields ?? new Dictionary<string, string>();
      _id = id;
   }

   public bool IsFlushing => RecursiveFlushGuard.IsFlushing;

   public void SetStudyingStatus(CardStudyingStatus status)
   {
      // Update card status: true = active/unsuspended, false = suspended
      _cardStatus[status.CardType] = !status.IsSuspended;
   }

   public NoteData GetData() => new(GetId(), _fields, Tags.ToInternedStringList());

   public override bool Equals(object? obj)
   {
      return obj is JPNote other && other.GetId() == _id;
   }

   public abstract void UpdateInCache();

   public bool IsStudying(string? cardType = null)
   {
      if(cardType == null)
      {
         // Return true if ANY card is active/unsuspended
         return _cardStatus.Any(kvp => kvp.Value);
      }

      // Return true if specific card type is active/unsuspended
      return _cardStatus.TryGetValue(cardType, out var isActive) && isActive;
   }

   public bool IsStudyingRead() => IsStudying(CardTypes.Reading);
   public bool IsStudyingListening() => IsStudying(CardTypes.Listening);

   public void SuspendAllCards()
   {
      Services.AnkiCardOperations.SuspendAllCardsForNote(_id);
      
      // Update local status for all known card types
      var cardTypes = _cardStatus.Keys.ToList();
      foreach (var cardType in cardTypes)
      {
         _cardStatus[cardType] = false; // false = suspended
      }
      
      Flush();
   }

   public void UnsuspendAllCards()
   {
      Services.AnkiCardOperations.UnsuspendAllCardsForNote(_id);
      
      // Update local status for all known card types
      var cardTypes = _cardStatus.Keys.ToList();
      foreach (var cardType in cardTypes)
      {
         _cardStatus[cardType] = true; // true = active/unsuspended
      }
      
      Flush();
   }

   public bool HasSuspendedCards()
   {
      // Return true if ANY card is suspended (value == false)
      return _cardStatus.Any(kvp => !kvp.Value);
   }

   public bool HasActiveCards() => IsStudying();

   public override int GetHashCode()
   {
      if(_hashValue == 0)
      {
         _hashValue = _id.GetHashCode();
         if(_hashValue == 0)
         {
            throw new InvalidOperationException("You cannot compare or hash a note that has not been saved yet since it has no id");
         }
      }

      return _hashValue;
   }

   public override string ToString() => $"{GetQuestion()}: {GetAnswer()}";

   public JPCollection Collection => Services.Collection;

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

   public NoteId GetId() => _id;

   public virtual void UpdateGeneratedData()
   {
      // Override in subclasses
   }

   public string GetField(string fieldName) => _fields.TryGetValue(fieldName, out var value) ? value : string.Empty;

   public void Flush()
   {
      RecursiveFlushGuard.Flush();
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
