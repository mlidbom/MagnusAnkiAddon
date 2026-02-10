using System;
using System.Collections.Generic;
using System.Linq;
using Avalonia.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Compze.Utilities.Logging;
using JAStudio.Core.Anki;
using JAStudio.Core.Configuration;

namespace JAStudio.UI.ViewModels;

public partial class ReadingsMappingsDialogViewModel : ObservableObject
{
   private readonly Window _window;
   private readonly Core.TemporaryServiceCollection _services;

   [ObservableProperty]
   private string _mappingsText = string.Empty;

   [ObservableProperty]
   private string _searchText = string.Empty;

   public RelayCommand SaveCommand { get; }
   public RelayCommand CancelCommand { get; }

   public ReadingsMappingsDialogViewModel(Window window, Core.TemporaryServiceCollection services)
   {
      _window = window;
      _services = services;

      _mappingsText = "\n" + _services.App.Config.ReadReadingsMappingsFile();

      SaveCommand = new RelayCommand(Save);
      CancelCommand = new RelayCommand(Cancel);
   }

   private void Save()
   {
      // Parse, deduplicate, and sort mappings
      var sorted = SortedValueLinesWithoutDuplicatesOrBlankLines();

      // Save to file
      _services.App.Config.SaveMappings(sorted);

      this.Log().Info("Readings mappings saved");
      _window.Close(true);

      // Refresh current note display to pick up new mappings
      AnkiFacade.UIUtils.Refresh();
   }

   private void Cancel()
   {
      _window.Close(false);
   }

   private string SortedValueLinesWithoutDuplicatesOrBlankLines()
   {
      var lines = MappingsText.Split('\n', StringSplitOptions.RemoveEmptyEntries);

      // Reverse so later entries override earlier ones
      lines = lines.Reverse().ToArray();

      // Parse into dictionary (key: value format)
      var mappings = new Dictionary<string, string>();
      foreach(var line in lines)
      {
         if(!line.Contains(':'))
            continue;

         var parts = line.Split(':', 2);
         if(parts.Length != 2)
            continue;

         var key = parts[0].Trim();
         var value = parts[1].Trim();

         if(string.IsNullOrWhiteSpace(key) || string.IsNullOrWhiteSpace(value))
            continue;

         mappings[key] = value;
      }

      // Convert back to sorted lines
      var sortedLines = mappings
                       .Select(kvp => $"{kvp.Key}:{kvp.Value}")
                       .OrderBy(line => line)
                       .ToList();

      return string.Join("\n", sortedLines);
   }
}
