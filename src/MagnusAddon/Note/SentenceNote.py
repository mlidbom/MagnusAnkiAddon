from anki.notes import Note

from Note.MyNote import MyNote


class SentenceNote(MyNote):
    def __init__(self, note: Note):
        super().__init__(note)
