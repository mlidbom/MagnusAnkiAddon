import tempfile
from os import path
from typing import Any

from anki.collection import Collection
from anki.models import NotetypeDict

from note.note_constants import NoteTypes, NoteFields


def test_create_collection() -> None:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        col = Collection(collection_file)

        try:
            add_note_type(col)
            cards = col.find_cards("*")
            print(cards)
        finally:
            col.close()


class MyNoteTemplate:
    def __init__(self, name: str):
        self.name = name
        self.ord = 0
        self.qfmt = "{{Tags}}"
        self.afmt = "{{Tags}}"
        self.bqfmt = ""
        self.bafmt = ""
        self.did = 0
        self.bfont = "Arial"
        self.bsize = 30

    def to_dict(self) -> dict[str, Any]:
        return {'name': self.name,
                'ord': self.ord,
                'qfmt': self.qfmt,
                'afmt': self.afmt,
                'bqfmt': self.bqfmt,
                'bafmt': self.bafmt,
                'did': self.did,
                'bfont': self.bfont,
                'bsize': self.bsize}


class MyNoteField:
    def __init__(self, name: str):
        self.name = name
        self.ord = 0
        self.sticky = False
        self.rtl = False
        self.font = 'Arial'
        self.size = 20
        self.description = ""
        self.plainText = False
        self.collapsed = False
        self.excludeFromSearch = False
        self.media: list[Any] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'ord': self.ord,
            'sticky': self.sticky,
            'rtl': self.rtl,
            'font': self.font,
            'size': self.size,
            'description': self.description,
            'plainText': self.plainText,
            'collapsed': self.collapsed,
            'excludeFromSearch': self.excludeFromSearch,
            'media': self.media}


class MyNoteType:
    def __init__(self, name: str, fields: list[MyNoteField], templates: list[MyNoteTemplate]):
        self.name = name
        self.id = 0
        self.flds = fields
        self.tmpls = templates
        self.type = 0
        self.mod = 0
        self.usn = 0
        self.sortf = 0
        self.did = 0
        self.css = ''
        self.latexPre = '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n'  # No clue, but 3 templates had this value
        self.latexPost = '\\end{document}'
        self.latexsvg = False
        self.req:list[Any] = []  # I have utterly no idea what this means. It is different for every note type. Seems to work empty even though no note type had these empty
        self.vers: list[Any] = []
        self.tags: list[Any] = []

        index = 0
        for field in self.flds:
            field.ord = index
            index += 1

        index = 0
        for template in self.tmpls:
            template.ord = index
            index += 1

    def to_dict(self) -> NotetypeDict:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'mod': self.mod,
            'usn': self.usn,
            'sortf': self.sortf,
            'did': self.did,
            'tmpls': [t.to_dict() for t in self.tmpls],
            'flds': [f.to_dict() for f in self.flds],
            'css': self.css,
            'latexPre': self.latexPre,
            'latexPost': self.latexPost,
            'latexsvg': self.latexsvg,
            'req': self.req,
            'vers': self.vers,
            'tags': self.tags
        }


japanese_sentence = {'id': 0,
                     'name': '_japanese_sentence',
                     'type': 0,
                     'mod': 0,
                     'usn': 0,
                     'sortf': 0,
                     'did': None,
                     'tmpls': [{'name': 'Listening',
                                'ord': 0,
                                'qfmt': '<div id="container1">\n   <div id="container2" class="{{Tags}} card{{Card}}">\n      <!--######-->\n      <div class="mainContent">\n         <div class="topSection">\n            <div>{{Audio Sentence}}</div>\n         </div>\n      </div>\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                                'afmt': '<div id="container1">\n   <div id="container2" class="{{Tags}} card{{Card}}">\n      <!--######-->\n      <div class="topSection">\n         <div>{{Audio Sentence}}</div>\n         <div class="image">{{Screenshot}}</div>\n\n         <div id="expressionAndReading">\n            {{#__question}}<div class="expression user clipboard">{{__question}}</div>{{/__question}}\n            <div class="expression clipboard {{#__question}}overridden{{/__question}}">{{source_question}}</div>\n            <div class="reading">{{furigana::Reading}}</div>\n         </div>\n\n         <div class="meaning user analysis clipboard">{{__answer_analysis}}</div>\n         <div class="meaning user clipboard">{{__answer}}</div>\n         <div class="meaning clipboard {{#__answer}}overridden{{/__answer}}">{{source_answer}}</div>\n      </div>\n\n      <div class="bottomSection">\n         {{#__comments}}<div class="user comments short">{{__comments}}</div>{{/__comments}}\n         {{#__comments_Long}}<div class="user comments long">{{__comments_Long}}</div>{{/__comments_Long}}\n         {{#Comments}}<div>{{Comments}}</div>{{/Comments}}\n      </div>\n\n      <div class="breakdown">\n         {{BreakDown}}\n      </div>\n\n      <div class="vocabList">\n         <div class="vocabEntry">{{__vocab1}}</div>\n         <div class="vocabEntry">{{__vocab2}}</div>\n         <div class="vocabEntry">{{__vocab3}}</div>\n         <div class="vocabEntry">{{__vocab4}}</div>\n         <div class="vocabEntry">{{__vocab5}}</div>\n      </div>\n\n      <div class="bottomSection">\n         {{#__references}}{{__references}}{{/__references}}\n         <div>\n            {{#__feedback-link}}<a href="{{__feedback-link}}">Sent feedback</a>{{/__feedback-link}}\n            {{#QuestionLink}}\n            {{^__feedback-link}}\n            <a href="mailto:joe@japanese-like-a-breeze.com?subject={{Version}}:{{Sequence}}">Mail feedback</a>\n            {{/__feedback-link}}\n            {{/QuestionLink}}\n         </div>\n\n         {{#References}}<div>{{References}}</div>{{/References}}\n      </div>\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                                'bqfmt': '',
                                'bafmt': '',
                                'did': None,
                                'bfont': 'Meiryo',
                                'bsize': 30},
                               {'name': 'Reading',
                                'ord': 1,
                                'qfmt': '<div id="container1">\n   <div id="container2" class="{{Tags}} card{{Card}}">\n      <!--######-->\n      <div class="expression">{{Q}}</div>\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                                'afmt': '<div id="container1">\n   <div id="container2" class="{{Tags}} card{{Card}}">\n      <!--######-->\n      <div class="topSection">\n         <div>{{Audio Sentence}}</div>\n         <div class="image">{{Screenshot}}</div>\n\n         <div id="expressionAndReading">\n            {{#__question}}<div class="expression user clipboard">{{__question}}</div>{{/__question}}\n            <div class="expression clipboard {{#__question}}overridden{{/__question}}">{{source_question}}</div>\n            <div class="reading">{{furigana::Reading}}</div>\n         </div>\n\n         <div class="meaning user analysis clipboard">{{__answer_analysis}}</div>\n         <div class="meaning user clipboard">{{__answer}}</div>\n         <div class="meaning clipboard {{#__answer}}overridden{{/__answer}}">{{source_answer}}</div>\n      </div>\n\n      <div class="bottomSection">\n         {{#__comments}}<div class="user comments short">{{__comments}}</div>{{/__comments}}\n         {{#__comments_Long}}<div class="user comments long">{{__comments_Long}}</div>{{/__comments_Long}}\n         {{#Comments}}<div>{{Comments}}</div>{{/Comments}}\n      </div>\n\n      <div class="breakdown">\n         {{BreakDown}}\n      </div>\n\n      <div class="vocabList">\n         <div class="vocabEntry">{{__vocab1}}</div>\n         <div class="vocabEntry">{{__vocab2}}</div>\n         <div class="vocabEntry">{{__vocab3}}</div>\n         <div class="vocabEntry">{{__vocab4}}</div>\n         <div class="vocabEntry">{{__vocab5}}</div>\n      </div>\n\n      <div class="bottomSection">\n         {{#__references}}{{__references}}{{/__references}}\n         <div>\n            {{#__feedback-link}}<a href="{{__feedback-link}}">Sent feedback</a>{{/__feedback-link}}\n            {{#QuestionLink}}\n            {{^__feedback-link}}\n            <a href="mailto:joe@japanese-like-a-breeze.com?subject={{Version}}:{{Sequence}}">Mail feedback</a>\n            {{/__feedback-link}}\n            {{/QuestionLink}}\n         </div>\n\n         {{#References}}<div>{{References}}</div>{{/References}}\n      </div>\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                                'bqfmt': '',
                                'bafmt': '',
                                'did': None,
                                'bfont': 'Meiryo',
                                'bsize': 30}],
                     'flds': [{'name': 'source_question', 'ord': 0, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 30, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': '__question', 'ord': 1, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 30, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': 'Reading', 'ord': 2, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 30, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'source_answer', 'ord': 3, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False},
                              {'name': '__answer_analysis', 'ord': 4, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False},
                              {'name': '__answer', 'ord': 5, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False},
                              {'name': 'CommentsFront', 'ord': 6, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'Comments', 'ord': 7, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False, 'media': []},
                              {'name': '__comments', 'ord': 8, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False},
                              {'name': '__comments_Long', 'ord': 9, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': '__feedback-link', 'ord': 10, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': '__references', 'ord': 11, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': '__vocab1', 'ord': 12, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': '__vocab2', 'ord': 13, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': '__vocab3', 'ord': 14, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': '__vocab4', 'ord': 15, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': '__vocab5', 'ord': 16, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': 'Version', 'ord': 17, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'Sequence', 'ord': 18, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'Source', 'ord': 19, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'Audio Sentence', 'ord': 20, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'Screenshot', 'ord': 21, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'QuestionLink', 'ord': 22, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'References', 'ord': 23, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                              {'name': 'iKnowID', 'ord': 24, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': 'iKnowType', 'ord': 25, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': 'ID', 'ord': 26, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': 'ParsedWords', 'ord': 27, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': 'BreakDown', 'ord': 28, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': 'A', 'ord': 29, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': 'Q', 'ord': 30, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False},
                              {'name': '__extra_vocab', 'ord': 31, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                              {'name': '__excluded_vocab', 'ord': 32, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False}],
                     'css': '@import url("__magnus_css_japanese_sentence.css");',
                     'latexPre': '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n',
                     'latexPost': '\\end{document}',
                     'latexsvg': False,
                     'req': [[0, 'any', [20]], [1, 'any', [30]]],
                     'vers': [],
                     'tags': []}  # noqa
kanji = {'id': 0,
         'name': '_Kanji',
         'type': 0,
         'mod': 0,
         'usn': 0,
         'sortf': 0,
         'did': 0,
         'tmpls': [{'name': 'Reading', 'ord': 0, 'qfmt': '<div id="container1">\n   <div id="container2">\n      <!--######-->\n\n      <div class="mainContent">\n         <div class="front-and-answer">\n            <div>\n               <div class="kanji">{{Q}}</div>\n            </div>\n         </div>\n      </div>\n\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>\n\n',
                    'afmt': '<div id="container1">\n   <div id="container2" class="{{Tags}} card{{Card}}">\n      <!--######-->\n\n      <div class="mainContent kanji{{Card}}">\n         <div class="front-and-answer">\n            <div class="kanjiContainer">\n               <div class="kanji">\n                  <span class="clipboard">{{Q}}</span>\n                  <span class="clipboard">{{#__similar_Characters}}!{{__similar_Characters}}{{/__similar_Characters}}</span>\n               </div>\n            </div>\n\n            {{#__primary_Vocab}}<div class="primaryVocab clipboard">{{__primary_Vocab}}</div>{{/__primary_Vocab}}\n            {{#__audio}}<div class="primaryVobabAudio">{{__audio}}</div>{{/__audio}}\n\n            {{#__references}}<div class="reference_url">{{__references}}</div>{{/__references}}\n\n            {{#__answer}}\n            <div class="meaning user">{{__answer}}</div>\n            {{/__answer}}\n            {{#__explanation}}\n            <div class="userExplanation">\t{{__explanation}}</div>\n            {{/__explanation}}\n\n            {{^__answer}}<div class="meaning">{{source_answer}}</div>{{/__answer}}\n\n            <div class="vocabList">\n               <div class="vocabEntry">{{__vocab1}}</div>\n               <div class="vocabEntry">{{__vocab2}}</div>\n               <div class="vocabEntry">{{__vocab3}}</div>\n            </div>\n\n            <div>\n               <div class="itemInfo">\n                  <div>\n                     <div class="text ">\n                        <span>On\'yomi:</span>\n                        <span class="reading">{{Reading_On}}</span>\n                     </div>\n\n                     <div class="text">\n                        <span>Kun\'yomi:</span>\n                        <span class="reading">{{Reading_Kun}}</span>\n                     </div>\n\n                     {{#__reading_Nan}}\n                     <div class="text">\n                        <span>Nanori:</span>\n                        <span class="reading">{{__reading_Nan}}</span>\n                     </div>\n                     {{/__reading_Nan}}\n                  </div>\n\n                  <div class="text">\n                     <span>Radicals:</span>\n                     <span class="radicals">{{Radicals}}</span>\n                     <span class="radical_icons">{{^Radicals_Icons}}, {{Radicals_Icons}}{{/Radicals_Icons}}</span>\n                     <span class="text">({{Radicals_Names}}{{#Radicals_Icons_Names}}, {{Radicals_Icons_Names}}{{/Radicals_Icons_Names}})</span>\n                  </div>\n               </div>\n            </div>\n         </div>\n         <div class="bottomSection">\n            <div>\n               {{#__mnemonic}}\n               <div class="mnemonics user">\n                  <div>{{__mnemonic}}</div>\n               </div>\n               {{/__mnemonic}}\n\n               {{^__mnemonic}}\n               <div>\n                  <div class="text">{{Meaning_Mnemonic}}</div>\n                  <div class="text hints">{{Meaning_Info}}</div>\n               </div>\n               <div>\n                  <div class="text">{{Reading_Mnemonic}}</div>\n                  <div class="text hints">{{Reading_Info}}</div>\n               </div>\n            </div>\n            {{/__mnemonic}}\n\n            {{Vocabs}}\n         </div>\n      </div>\n\n      <div class="referenceLink">\n         <a target="_blank" href="https://www.wanikani.com/kanji/{{Q}}">Wanikani</a>\n         <a target="_blank" href="https://jisho.org/search/{{Q}}%20%23kanji">Jisho(kanji)</a>\n         <a target="_blank" href="https://jisho.org/search/*{{Q}}*">Jisho(vocab)</a>\n         <a target="_blank" href="https://www.immersionkit.com/dictionary?keyword={{Q}}&exact=true&sort=shortness">Immersion Kit</a>\n         Tags:{{Tags}}\n      </div>\n\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>\n\n',
                    'bqfmt': '',
                    'bafmt': '',
                    'did': 1686827724395,
                    'bfont': 'Meiryo',
                    'bsize': 30}],
         'flds': [{'name': 'Q', 'ord': 0, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 40, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False, 'media': []},
                  {'name': 'source_answer', 'ord': 1, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Reading_On', 'ord': 2, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Reading_Kun', 'ord': 3, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': '__primary_Vocab', 'ord': 4, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 30, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__audio', 'ord': 5, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__references', 'ord': 6, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__answer', 'ord': 7, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__mnemonic', 'ord': 8, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__explanation', 'ord': 9, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__similar_Characters', 'ord': 10, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__reading_Nan', 'ord': 11, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__vocab1', 'ord': 12, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__vocab2', 'ord': 13, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__vocab3', 'ord': 14, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'Radicals', 'ord': 15, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 40, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Radicals_Icons', 'ord': 16, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Radicals_Names', 'ord': 17, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Radicals_Icons_Names', 'ord': 18, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Meaning_Mnemonic', 'ord': 19, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Meaning_Info', 'ord': 20, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Reading_Mnemonic', 'ord': 21, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Reading_Info', 'ord': 22, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Vocabulary', 'ord': 23, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'sort_id', 'ord': 24, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'subject_id', 'ord': 25, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'level', 'ord': 26, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'lesson_position', 'ord': 27, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'document_url', 'ord': 28, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'my_learning_order', 'ord': 29, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'amalgamation_subject_ids', 'ord': 30, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'component_subject_ids', 'ord': 31, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'auxiliary_meanings_whitelist', 'ord': 32, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'auxiliary_meanings_blacklist', 'ord': 33, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'Vocabs', 'ord': 34, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'VocabsRaw', 'ord': 35, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'A', 'ord': 36, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False}],
         'css': '@import url("__magnus_css_wanikani_kanji.css");', 'latexPre': '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n',
         'latexPost': '\\end{document}',
         'latexsvg': False,
         'req': [[0, 'any', [0]]],
         'tags': [],
         'vers': []}  # noqa

radical = {'id': 0,
           'name': '_Radical',
           'type': 0,
           'mod': 0,
           'usn': 0,
           'sortf': 0,
           'did': 0,
           'tmpls': [{'name': 'Recognition',
                      'ord': 0,
                      'qfmt': '<div id="container1">\n   <div id="container2" class="{{Tags}} card{{Card}}">\n      <!--######-->\n\n      <div class="mainContent">\n         <div class="front-and-answer">\n            <div class="kanji">{{Q}}<span class="radicon">{{Radical_Icon}}</span></div>\n         </div>\n      </div>\n\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                      'afmt': '<div id="container1">\n   <div id="container2">\n      <!--######-->\n\n      <div class="mainContent">\n         <div class="front-and-answer">\n            <div>\n               <div class="kanji">\n                  {{Q}}<span class="radicon">{{Radical_Icon}}</span>\n                  {{#Similar_Radicals}} !{{Similar_Radicals}} {{/Similar_Radicals}}\n               </div>\n            </div>\n\n            <div>\n               <div>\n                  <div class="text radicalName">{{A}}</div>\n                  <div>\n                     <a class="referenceLink" target="_blank" href="https://www.wanikani.com/radicals/{{A}}">Wanikani</a>\n                     <a class="referenceLink" target="_blank" href="https://jisho.org/search/{{Q}}%20%23kanji">Jisho</a>\n                     <a class="referenceLink" target="_blank" href="https://www.immersionkit.com/dictionary?keyword={{Q}}&exact=true&sort=shortness">Anime Sentences</a>\n                  </div>\n               </div>\n            </div>\n         </div>\n         <div class="bottomSection">\n            {{#__mnemonic}}\n            <div class="mnemonics user" ">\n               <div class="text">{{__mnemonic}}</div>\n            </div>\n            {{/__mnemonic}}\n            {{^__mnemonic}}\n            <div class="mnemonics" ">\n               <div>\n                  <span class="text">{{Radical_Meaning}}</span>\n               </div>\n            </div>\n            {{/__mnemonic}}\n         </div>\n      </div>\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                      'bqfmt': '',
                      'bafmt': '',
                      'did': None,
                      'bfont': 'Meiryo',
                      'bsize': 30}],
           'flds': [{'name': 'Q', 'ord': 0, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 40, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False, 'media': []},
                    {'name': 'A', 'ord': 1, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False, 'media': []},
                    {'name': 'Radical_Meaning', 'ord': 2, 'sticky': False, 'rtl': False, 'font': 'Liberation Sans', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False, 'media': []},
                    {'name': '__mnemonic', 'ord': 3, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False},
                    {'name': 'Radical_Icon', 'ord': 4, 'sticky': False, 'rtl': False, 'font': 'Liberation Sans', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False, 'media': []},
                    {'name': 'Similar_Radicals', 'ord': 5, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False},
                    {'name': 'sort_id', 'ord': 6, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                    {'name': 'subject_id', 'ord': 7, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                    {'name': 'level', 'ord': 8, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                    {'name': 'lesson_position', 'ord': 9, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                    {'name': 'document_url', 'ord': 10, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                    {'name': 'my_learning_order', 'ord': 11, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                    {'name': 'amalgamation_subject_ids', 'ord': 12, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                    {'name': 'auxiliary_meanings_whitelist', 'ord': 13, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                    {'name': 'auxiliary_meanings_blacklist', 'ord': 14, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False}],
           'css': '@import "__magnus_css_wanikani_radical.css";',
           'latexPre': '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n',
           'latexPost': '\\end{document}',
           'latexsvg': False,
           'req': [[0, 'any', [0, 4]]],
           'tags': [],
           'vers': []}  # noqa
vocab = {'id': 0,
         'name': '_Vocab',
         'type': 0,
         'mod': 0,
         'usn': 2674,
         'sortf': 0,
         'did': 0,
         'tmpls': [{'name': 'Listening',
                    'ord': 0,
                    'qfmt': '<div id="container1">\n   <div id="container2">\n      <!--######-->\n      \n      <div class="front-and-answer">\n         <div>{{Audio_g}}{{Audio_b}}</div>\n      </div>\n\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                    'afmt': '<div id="container1">\n   <div id="container2" class="\n        {{Tags}}\n        card{{Card}}\n        {{#__explanation}}has__explanation{{/__explanation}}\n        {{#__explanation_long}}has__explanation_long{{/__explanation_long}}\n        ">\n      <!--######-->\n\n      <div class="front-and-answer">\n         <div>\n            <div class="question">\n               <div>\n                  <span class="clipboard">{{Q}}</span>\n                  {{#__derivedFrom}}&lt; <span class="derivedFrom clipboard">{{__derivedFrom}}</span>{{/__derivedFrom}}\n                  {{#__ergative_twin}}~<span class="ergativeTwin clipboard">{{__ergative_twin}}</span>{{/__ergative_twin}}\n                  {{#__confused_with}}!<span class="similarVocab clipboard">{{__confused_with}}</span>{{/__confused_with}}\n                  {{#__similar_meaning}}:<span class="similarMeaning clipboard">{{__similar_meaning}}</span>{{/__similar_meaning}}\n               </div>\n               {{#Kanji_Name}}<div class="kanjiNames">{{Kanji_Name}}</div>{{/Kanji_Name}}\n            </div>\n         </div>\n         {{#__references}}<div class="referenceLink">{{__references}}</div>{{/__references}}\n         <div>{{Audio_g}}{{Audio_b}}</div>\n\n         {{#__answer}}<div class="meaning user">{{__answer}}</div>{{/__answer}}\n         {{^__answer}}<div class="meaning"> {{source_answer}}</div>{{/__answer}}\n\n         <div class="metaData">\n            <span class="_derog">derog</span>\n            <span class="_uk" title="usually kana only">uk</span>\n            <span class="_masustem">masu stem</span>\n            <span class="partOfSpeech">{{Speech_Type}}</span>\n            <span class="reading clipboard">{{Reading}}</span>\n         </div>\n         {{#Homophones}}<div id="homophonesDiv">Homophones: {{Homophones}} </div>{{/Homophones}}\n         {{#__explanation}}<div id="__explanation" class="user">{{__explanation}}</div>{{/__explanation}}\n      </div>\n\n      {{#__image}}<div class="image">{{__image}}</div>{{/__image}}\n      {{#Image}}<div class="image">{{Image}}</div>{{/Image}}\n    \n   <div class="vocabList">\n      {{#__vocab1}}<div class="vocabEntry replacement">{{__vocab1}}</div>{{/__vocab1}}\n      {{#__vocab2}}<div class="vocabEntry context">{{__vocab2}}</div>{{/__vocab2}}\n      {{#__vocab3}}<div class="vocabEntry context">{{__vocab3}}</div>{{/__vocab3}}\n      {{#__vocab4}}<div class="vocabEntry context">{{__vocab4}}</div>{{/__vocab4}}\n      {{#__vocab5}}<div class="vocabEntry context">{{__vocab5}}</div>{{/__vocab5}}\n   </div>\n      \n\n      <div class="bottomSection">\n         {{#__explanation_long}}<div id="__explanation_long" class="user">{{__explanation_long}}</div>{{/__explanation_long}}\n         {{#__mnemonic}}\n         <div>\n            <div class="mnemonic override">{{__mnemonic}}</div>\n         </div>\n         {{/__mnemonic}}\n\n\n         {{^__mnemonic}}\n         <div>\n            {{#Meaning_Exp}}<div class="mnemonic">{{Meaning_Exp}}</div>{{/Meaning_Exp}}\n\n            <br>\n\n            {{#Reading_Exp}}\n            <div>\n               <div class="mnemonic">{{Reading_Exp}}</div>\n            </div>\n            {{/Reading_Exp}}\n\n            <br>\n         </div>\n         {{/__mnemonic}}\n\n         <div class="context list">\n            {{#Context_jp}}\n            <div class="context">\n               <div class="context_jp clipboard">{{Context_jp}}</div>\n               <div>{{Context_en}}</div>\n            </div>\n            {{/Context_jp}}\n\n            {{#Context_jp_2}}\n            <div class="context">\n               <div class="context_jp clipboard">{{Context_jp_2}}</div>\n               <div>{{Context_en_2}}</div>\n            </div>\n            {{/Context_jp_2}}\n\n            {{#Context_jp_3}}\n            <div class="context">\n               <div class="context_jp clipboard">{{Context_jp_3}}</div>\n               <div>{{Context_en_3}}</div>\n            </div>\n            {{/Context_jp_3}}\n\n         </div>\n      </div>\n      <div class="tags">{{Tags}}</div>\n\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                    'bqfmt': '',
                    'bafmt': '',
                    'did': 1686827715804,
                    'bfont': 'Meiryo',
                    'bsize': 30},
                   {'name': 'Reading',
                    'ord': 1,
                    'qfmt': '<div id="container1">\n   <div id="container2">\n      <!--######-->\n      \n      <div class="front-and-answer">\n         <div class="question">{{Q}}</div>\n      </div>\n\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                    'afmt': '<div id="container1">\n   <div id="container2" class="\n        {{Tags}}\n        card{{Card}}\n        {{#__explanation}}has__explanation{{/__explanation}}\n        {{#__explanation_long}}has__explanation_long{{/__explanation_long}}\n        ">\n      <!--######-->\n\n      <div class="front-and-answer">\n         <div>\n            <div class="question">\n               <div>\n                  <span class="clipboard">{{Q}}</span>\n                  {{#__derivedFrom}}&lt; <span class="derivedFrom clipboard">{{__derivedFrom}}</span>{{/__derivedFrom}}\n                  {{#__ergative_twin}}~<span class="ergativeTwin clipboard">{{__ergative_twin}}</span>{{/__ergative_twin}}\n                  {{#__confused_with}}!<span class="similarVocab clipboard">{{__confused_with}}</span>{{/__confused_with}}\n                  {{#__similar_meaning}}:<span class="similarMeaning clipboard">{{__similar_meaning}}</span>{{/__similar_meaning}}\n               </div>\n               {{#Kanji_Name}}<div class="kanjiNames">{{Kanji_Name}}</div>{{/Kanji_Name}}\n            </div>\n         </div>\n         {{#__references}}<div class="referenceLink">{{__references}}</div>{{/__references}}\n         <div>{{Audio_g}}{{Audio_b}}</div>\n\n         {{#__answer}}<div class="meaning user">{{__answer}}</div>{{/__answer}}\n         {{^__answer}}<div class="meaning"> {{source_answer}}</div>{{/__answer}}\n\n         <div class="metaData">\n            <span class="_derog">derog</span>\n            <span class="_uk" title="usually kana only">uk</span>\n            <span class="_masustem">masu stem</span>\n            <span class="partOfSpeech">{{Speech_Type}}</span>\n            <span class="reading clipboard">{{Reading}}</span>\n         </div>\n         {{#Homophones}}<div id="homophonesDiv">Homophones: {{Homophones}} </div>{{/Homophones}}\n         {{#__explanation}}<div id="__explanation" class="user">{{__explanation}}</div>{{/__explanation}}\n      </div>\n\n      {{#__image}}<div class="image">{{__image}}</div>{{/__image}}\n      {{#Image}}<div class="image">{{Image}}</div>{{/Image}}\n    \n   <div class="vocabList">\n      {{#__vocab1}}<div class="vocabEntry replacement">{{__vocab1}}</div>{{/__vocab1}}\n      {{#__vocab2}}<div class="vocabEntry context">{{__vocab2}}</div>{{/__vocab2}}\n      {{#__vocab3}}<div class="vocabEntry context">{{__vocab3}}</div>{{/__vocab3}}\n      {{#__vocab4}}<div class="vocabEntry context">{{__vocab4}}</div>{{/__vocab4}}\n      {{#__vocab5}}<div class="vocabEntry context">{{__vocab5}}</div>{{/__vocab5}}\n   </div>\n      \n\n      <div class="bottomSection">\n         {{#__explanation_long}}<div id="__explanation_long" class="user">{{__explanation_long}}</div>{{/__explanation_long}}\n         {{#__mnemonic}}\n         <div>\n            <div class="mnemonic override">{{__mnemonic}}</div>\n         </div>\n         {{/__mnemonic}}\n\n\n         {{^__mnemonic}}\n         <div>\n            {{#Meaning_Exp}}<div class="mnemonic">{{Meaning_Exp}}</div>{{/Meaning_Exp}}\n\n            <br>\n\n            {{#Reading_Exp}}\n            <div>\n               <div class="mnemonic">{{Reading_Exp}}</div>\n            </div>\n            {{/Reading_Exp}}\n\n            <br>\n         </div>\n         {{/__mnemonic}}\n\n         <div class="context list">\n            {{#Context_jp}}\n            <div class="context">\n               <div class="context_jp clipboard">{{Context_jp}}</div>\n               <div>{{Context_en}}</div>\n            </div>\n            {{/Context_jp}}\n\n            {{#Context_jp_2}}\n            <div class="context">\n               <div class="context_jp clipboard">{{Context_jp_2}}</div>\n               <div>{{Context_en_2}}</div>\n            </div>\n            {{/Context_jp_2}}\n\n            {{#Context_jp_3}}\n            <div class="context">\n               <div class="context_jp clipboard">{{Context_jp_3}}</div>\n               <div>{{Context_en_3}}</div>\n            </div>\n            {{/Context_jp_3}}\n\n         </div>\n      </div>\n      <div class="tags">{{Tags}}</div>\n\n      <!--######-->\n   </div>\n</div>\n\n<script src="__magnus_js.js"></script>',
                    'bqfmt': '',
                    'bafmt': '',
                    'did': 1686827724395,
                    'bfont': 'Meiryo',
                    'bsize': 30}],
         'flds': [{'name': 'Q', 'ord': 0, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 40, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'F', 'ord': 1, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'source_answer', 'ord': 2, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Reading', 'ord': 3, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Speech_Type', 'ord': 4, 'sticky': False, 'rtl': False, 'font': 'Liberation Sans', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Audio_b', 'ord': 5, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Audio_g', 'ord': 6, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': '__variations', 'ord': 7, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__answer', 'ord': 8, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__references', 'ord': 9, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__explanation', 'ord': 10, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__explanation_long', 'ord': 11, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__mnemonic', 'ord': 12, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__confused_with', 'ord': 13, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__ergative_twin', 'ord': 14, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__derivedFrom', 'ord': 15, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__similar_meaning', 'ord': 16, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'Homophones', 'ord': 17, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__vocab1', 'ord': 18, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__vocab2', 'ord': 19, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__vocab3', 'ord': 20, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__vocab4', 'ord': 21, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': '__vocab5', 'ord': 22, 'sticky': False, 'rtl': False, 'font': 'Meiryo UI', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'Image', 'ord': 23, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': False, 'excludeFromSearch': False},
                  {'name': '__image', 'ord': 24, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'Meaning_Exp', 'ord': 25, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Reading_Exp', 'ord': 26, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Context_jp', 'ord': 27, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Context_en', 'ord': 28, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Context_jp_2', 'ord': 29, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Context_en_2', 'ord': 30, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Context_jp_3', 'ord': 31, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Context_en_3', 'ord': 32, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Kanji', 'ord': 33, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'Kanji_Name', 'ord': 34, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'sort_id', 'ord': 35, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False, 'media': []},
                  {'name': 'subject_id', 'ord': 36, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'level', 'ord': 37, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'lesson_position', 'ord': 38, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'document_url', 'ord': 39, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'my_learning_order', 'ord': 40, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'component_subject_ids', 'ord': 41, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'auxiliary_meanings_whitelist', 'ord': 42, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'auxiliary_meanings_blacklist', 'ord': 43, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'iKnowType', 'ord': 44, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'iKnowID', 'ord': 45, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'ParsedTypeOfSpeech', 'ord': 46, 'sticky': False, 'rtl': False, 'font': 'Meiryo', 'size': 20, 'description': '', 'plainText': True, 'collapsed': True, 'excludeFromSearch': False},
                  {'name': 'A', 'ord': 47, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'description': '', 'plainText': False, 'collapsed': True, 'excludeFromSearch': False}],
         'css': '@import url("__magnus_css_wanikani_vocab.css");',
         'latexPre': '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n',
         'latexPost': '\\end{document}',
         'latexsvg': False,
         'req': [[0, 'any', [5, 6]], [1, 'any', [0]]],
         'vers': [],
         'tags': []}  # noqa


def add_note_type(col: Collection) -> None:
    col.models.add(japanese_sentence)
    col.models.add(kanji)
    col.models.add(radical)
    col.models.add(vocab)
    col.save()


def create_vocab() -> MyNoteType:
    return MyNoteType(NoteTypes.Vocab,
                      [MyNoteField(NoteFields.Vocab.question),
                       MyNoteField(NoteFields.Vocab.active_answer),
                       MyNoteField(NoteFields.Vocab.source_answer),
                       MyNoteField(NoteFields.Vocab.user_answer),
                       MyNoteField(NoteFields.Vocab.Reading),
                       MyNoteField(NoteFields.Vocab.Speech_Type),
                       MyNoteField(NoteFields.Vocab.Context_jp),
                       MyNoteField(NoteFields.Vocab.Context_en),
                       MyNoteField(NoteFields.Vocab.Context_jp_2),
                       MyNoteField(NoteFields.Vocab.Context_en_2),
                       MyNoteField(NoteFields.Vocab.Context_jp_3),
                       MyNoteField(NoteFields.Vocab.Context_en_3),
                       MyNoteField(NoteFields.Vocab.Meaning_Exp),
                       MyNoteField(NoteFields.Vocab.Audio_b),
                       MyNoteField(NoteFields.Vocab.Audio_g),
                       MyNoteField(NoteFields.Vocab.sort_id),
                       MyNoteField(NoteFields.Vocab.Related_homophones),
                       MyNoteField(NoteFields.Vocab.Related_similar_meaning),
                       MyNoteField(NoteFields.Vocab.Related_derived_from),
                       MyNoteField(NoteFields.Vocab.Related_ergative_twin),
                       MyNoteField(NoteFields.Vocab.Related_confused_with),
                       MyNoteField(NoteFields.Vocab.Kanji),
                       MyNoteField(NoteFields.Vocab.Forms),
                       MyNoteField(NoteFields.Vocab.Kanji_Name),
                       MyNoteField(NoteFields.Vocab.Reading_Exp),
                       MyNoteField(NoteFields.Vocab.Homophones),
                       MyNoteField(NoteFields.Vocab.ParsedTypeOfSpeech),
                       MyNoteField(NoteFields.Vocab.Mnemonic__),
                       MyNoteField(NoteFields.Vocab.component_subject_ids)],
                      [MyNoteTemplate("listening")])


_minimal_note_type = {'id': 0,
                     'name': '_japanese_sentence',
                     'type': 0,
                     'mod': 0,
                     'usn': 0,
                     'sortf': 0,
                     'did': 0,
                     'tmpls': [{'name': 'Listening',
                                'ord': 0,
                                'qfmt': '{{Tags}}',
                                'afmt': '{{Tags}}',
                                'bqfmt': '',
                                'bafmt': '',
                                'did': 0,
                                'bfont': 'Arial',
                                'bsize': 30}],
                     'flds': [{'name': '__question',
                               'ord': 0,
                               'sticky': False,
                               'rtl': False,
                               'font': 'Arial',
                               'size': 20,
                               'description': '',
                               'plainText': False,
                               'collapsed': False,
                               'excludeFromSearch': False,
                               'media': []}],
                     'css': '',
                     'latexPre': '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n',
                     'latexPost': '\\end{document}',
                     'latexsvg': False,
                     'req': [],
                     'vers': [],
                     'tags': []}  # noqa

def test_create_minimal_note_type() -> None:
    created = create_vocab()
    with tempfile.TemporaryDirectory() as tmp_dirname:
        collection_file = path.join(tmp_dirname, "collection.anki2")
        col = Collection(collection_file)

        try:
            col.models.add_dict(created.to_dict())
        finally:
            col.close()
