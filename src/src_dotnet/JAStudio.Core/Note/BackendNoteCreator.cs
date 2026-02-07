using System;
using JAStudio.Core.Anki;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.Core.Note;

public interface IBackendNoteCreator
{
   void CreateKanji(KanjiNote note, Action callback);
   void CreateVocab(VocabNote note, Action callback);
   void CreateSentence(SentenceNote note, Action callback);
}

internal class AnkiBackendNoteCreator : IBackendNoteCreator
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

public class TestingBackendNoteCreator : IBackendNoteCreator
{
   private int _currentId;

   private int GetNextId()
   {
      _currentId++;
      return _currentId;
   }

   public void CreateKanji(KanjiNote note, Action callback)
   {
      note.SetId(GetNextId());
      callback();
   }

   public void CreateVocab(VocabNote note, Action callback)
   {
      note.SetId(GetNextId());
      callback();
   }

   public void CreateSentence(SentenceNote note, Action callback)
   {
      note.SetId(GetNextId());
      callback();
   }
}
