using System;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.Anki;

public class AnkiBackendNoteCreator : IBackendNoteCreator
{
   readonly PythonObjectWrapper _noteCreator;

   public AnkiBackendNoteCreator()
   {
      using(PythonEnvironment.LockGil())
      {
         dynamic noteCreatorModule = Py.Import("jastudio.note.anki_backend_note_creator");
         _noteCreator = new PythonObjectWrapper(noteCreatorModule.AnkiBackendNoteCreator());
      }
   }

   public void CreateKanji(KanjiNote note, Action callback) => _noteCreator.Use(it => it.create_kanji(note));

   public void CreateVocab(VocabNote note, Action callback) => _noteCreator.Use(it => it.create_vocab(note));

   public void CreateSentence(SentenceNote note, Action callback) => _noteCreator.Use(it => it.create_sentence(note));
}
