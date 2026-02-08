using System;

namespace JAStudio.Core.TaskRunners;

/// <summary>
/// Controls the degree of parallelism for <see cref="ITaskProgressRunner.ProcessWithProgressAsync{TInput,TOutput}"/>.
/// </summary>
public record Parallelism
{
   public static readonly Parallelism Sequential = new(1);
   public static readonly Parallelism AllCores = new(Environment.ProcessorCount);
   public static readonly Parallelism HalfCores = new(Math.Max(1, Environment.ProcessorCount / 2));

   public static Parallelism FractionOfCores(double fraction) =>
      new(Math.Max(1, (int)(Environment.ProcessorCount * fraction)));

   public static Parallelism Cores(int count) => new(Math.Max(1, count));

   public int Threads { get; }

   Parallelism(int threads) => Threads = threads;
}
