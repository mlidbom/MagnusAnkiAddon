from aqt.utils import showInfo

from note.kanjinote import KanjiNote
from note.note_constants import Mine
from note.radicalnote import RadicalNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from ankiutils import app
from wanikani.wanikani_api_client import WanikaniClient

waniClient = WanikaniClient.get_instance()


def import_missing_radicals() -> None:
    all_radicals: list[RadicalNote] = app.col().radicals.all()
    local_radicals_dictionary = {radical.get_subject_id(): radical for radical in all_radicals}
    all_wani_radicals = waniClient.list_radicals()
    imported = 0
    for wani_radical in all_wani_radicals:
        if wani_radical.id not in local_radicals_dictionary:
            print("Importing: {}".format(wani_radical.slug))
            RadicalNote.create_from_wani_radical(wani_radical)
            imported += 1

    showInfo("Imported {} radical notes".format(imported))


def import_missing_kanji() -> None:
    all_kanji: list[KanjiNote] = app.col().kanji.all_wani()
    local_kanji_dictionary = {kanji.get_subject_id(): kanji for kanji in all_kanji}
    all_wani_kanji = waniClient.list_kanji()
    imported = 0
    for wani_kanji in all_wani_kanji:
        if wani_kanji.id not in local_kanji_dictionary:
            print("Importing: {}".format(wani_kanji.slug))
            KanjiNote.create_from_wani_kanji(wani_kanji)
            imported += 1

    showInfo("Imported {} kanji notes".format(imported))


def import_missing_vocab() -> None:
    all_wani_vocabulary = waniClient.list_vocabulary()
    imported = 0
    for wani_vocab in all_wani_vocabulary:
        question = str(wani_vocab.characters)
        if not app.col().vocab.with_question(question):
            print(f"""Importing: {wani_vocab.slug}""")
            VocabNote.create_from_wani_vocabulary(wani_vocab)
            imported += 1

    showInfo(f"""Imported {imported} vocabulary notes""")

def import_missing_context_sentences() -> None:
    sentence_collection = app.col().sentences
    all_wani_vocabulary = waniClient.list_vocabulary()
    imported_sentences:set[SentenceNote] = set()
    present = 0
    for wani_vocab in all_wani_vocabulary:
        for sentence in wani_vocab.context_sentences:
            vocab = str(wani_vocab.characters)
            question = str(sentence.japanese)
            answer = str(sentence.english).strip()

            existing_sentences = sentence_collection.with_question(question)
            if not existing_sentences:
                sentence_collection.with_question(question.strip())

            if not existing_sentences:
                print(f"""Importing {vocab} :: {question} || {answer}""")
                imported_sentences.add(SentenceNote.add_sentence(question=question.strip(), answer=answer, highlighted_vocab={vocab}, tags={Mine.Tags.Wani, Mine.Tags.wani_sentence_current}))
            else:
                for existing in existing_sentences:
                    existing.set_tag(Mine.Tags.wani_sentence_current)
                present += 1

    old_sentences = [sent for sent in app.col().sentences.all() if sent.has_tag(Mine.Tags.Wani) and not sent.has_tag(Mine.Tags.wani_sentence_current)]
    for old_sentence in old_sentences:
        old_sentence.remove_tag(Mine.Tags.wani_sentence_current)
        old_sentence.set_tag(Mine.Tags.wani_sentence_removed_on_wani)

    print(f'''Imported: {len(imported_sentences)} sentences.''')
    print(f'''Already present: {present} sentences.''')
    print(f'''Marked as removed: {len(old_sentences)} sentences.''')
