* We have stuff checking for .IsEmpty on our Id classes. This should be impossible. No such thing as an empty ID. Guarantee it in the class.
* 

* NoteBulkLoader.cs 
    * not to sure about this kind of thing.... I don't really trust it to be globally unique
        ```
          // Generate a deterministic Guid from the Anki note ID for cross-session stability.
          // This will be replaced by reading from a jp_note_id field once that migration is done.
-         var noteId = new NoteId(Guid.CreateVersion5(AnkiIdNamespace, BitConverter.GetBytes(ankiId)));
+         var noteId = new NoteId(NoteId.DeterministicGuidFromAnkiId(ankiId));
        ```