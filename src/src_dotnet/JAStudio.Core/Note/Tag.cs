using System.Collections.Generic;
using Compze.Utilities.SystemCE.ThreadingCE;
using Compze.Utilities.SystemCE.ThreadingCE.ResourceAccess;

namespace JAStudio.Core.Note;

public class Tag
{
   static readonly IMonitorCE _monitor = IMonitorCE.WithDefaultTimeout();
   static HashSet<int> _usedIds = [];
   static Dictionary<int, Tag> _byId = new();
   static Dictionary<string, Tag> _byName = new();

   public string Name { get; }
   public int Id { get; }
   public long Bit { get; }

   Tag(string name)
   {
      var id = _usedIds.Count;

      Name = name;
      Id = id;
      Bit = 1L << id;
   }

   static void RegisterTag(string name)
   {
      var created = new Tag(name);
      _usedIds = _usedIds.AddToCopy(created.Id);
      _byId = _byId.AddToCopy(created.Id, created);
      _byName = _byName.AddToCopy(name, created);
   }

   public static Tag FromName(string name) =>
      _monitor.DoubleCheckedLocking(() => _byName!.GetValueOrDefault(name, null),
                                    () => RegisterTag(name));

   public static Tag FromId(int id) => _byId[id];
}
