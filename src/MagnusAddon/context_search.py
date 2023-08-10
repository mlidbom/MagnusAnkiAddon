# coding: utf-8

"""
Anki Add-on: Reviewer Context Menu Search

Adds context menu entries for searching various online search providers.

You can customize the menu entries for online providers by
editing the SEARCH_PROVIDERS list below.

Based on:
'Context Menu Search' by Glutanimate
'OSX Dictionary Lookup' by Eddie Blundell, 
'Search Google Images' by Steve AW,
"""
from magnus import my_clipboard

############## USER CONFIGURATION START ##############

# list of tuples of search provider names and urls.
# '%s' will be replaced with the search term
SEARCH_PROVIDERS = [
    ("&Takoboto", [u"https://takoboto.jp/?q=%s"]),
    ("&Jisho", [u"https://jisho.org/search/%s"]),
    ("&Wanikani", [u"https://www.wanikani.com/search?query=%s"]),
    ("&Verbix conjugate", [u"https://www.verbix.com/webverbix/japanese/%s"]),
    ("&Japanese verb conjugator", [u"https://www.japaneseverbconjugator.com/VerbDetails.asp?Go=Conjugate&txtVerb=%s"]),
    ("&Immersion Kit", [u"https://www.immersionkit.com/dictionary?exact=true&sort=shortness&keyword=%s"]),
    ("&Deepl", [u"https://www.deepl.com/en/translator#ja/en/%s"]),
    ("&Merriam Webster", [u"https://www.merriam-webster.com/dictionary/%s"])
]

##############  USER CONFIGURATION END  ##############

import urllib

import aqt
from aqt.qt import *
from aqt.utils import openLink
from anki.hooks import addHook

def lookup_online(text, idx):
#    text = " ".join(text.split())
    text = urllib.parse.quote(text, encoding='utf8')
    for url in SEARCH_PROVIDERS[idx][1]:
        openLink(url % text)    

def add_lookup_action(view, menu):
    """Add 'lookup' action to context menu"""
    selected = view.page().selectedText().strip()
    if not selected:
        selected = my_clipboard.get_text()
        if not selected:
            return
    
    suffix = (selected[:20] + '..') if len(selected) > 20 else selected

    search_menu = menu.addMenu(f'&Web search')

    for idx, provider in enumerate(SEARCH_PROVIDERS):
        label = provider[0]
        a = search_menu.addAction(label)
        a.triggered.connect(lambda _, i=idx,t=selected: lookup_online(t, i))
