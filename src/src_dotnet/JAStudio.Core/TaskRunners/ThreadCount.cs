using System;
using System.Threading.Tasks;

namespace JAStudio.Core.TaskRunners;

public class ThreadCount
{
   public static readonly ThreadCount One = new(1);
   public static readonly ThreadCount AllLogicalCores = new(Environment.ProcessorCount);
   public static readonly ThreadCount HalfLogicalCores = new(Math.Max(1, Environment.ProcessorCount / 2));

   public static ThreadCount FractionOfLogicalCores(double fraction) => new(Math.Max(1, (int)(Environment.ProcessorCount * fraction)));

   public static ThreadCount WithThreads(int count) => new(Math.Max(1, count));

   public int Threads { get; }

   public bool IsSequential => Threads == 1;

   public ParallelOptions ParallelOptions => new() { MaxDegreeOfParallelism = Threads };

   ThreadCount(int threads)
   {
      if(threads < 1) throw new ArgumentException("Thread count must be positive", nameof(threads));
      Threads = threads;
   }
}
