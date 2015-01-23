# -*- coding: utf-8 -*-
"""
This package contains implementations of proper RYM capitalization.

Please be noticed that only English capitalization is more or less supported
because it is too hard to recognize language of title based on short texts.
By default title is considered as English one. Russian capitalization is
supported so-so, spanish is more or less suits the needs but anyway, since
natural language processing is rather hard it is better not to expect
absolutely valid results in all cases here.

We cannot trust other titles because there is a common practice that artists
put names in all possible languages.

So do not forget to fix some minor problems by yourself. This module just
tries to reduce your pain.
"""


from __future__ import absolute_import, unicode_literals

import itertools
import re

import nltk
import nltk.data
import nltk.corpus
import six

from .english import EnglishCapitalization
from .dutch import DutchCapitalization
from .russian import RussianCapitalization
from .spanish import SpanishCapitalization


PRECALCULATED_LANGSETS = {}

CYRILLIC_ALPHABET = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬЬБЮ"
CYRILLIC_ALPHABET = frozenset(CYRILLIC_ALPHABET + CYRILLIC_ALPHABET.lower())

FIX_PUNCTUATION = re.compile(r"\s+(?=[\.,!?:;])")
SEPARATORS = re.compile(r"([\[\]\(\)'\"\{\}\.,?!:;])")
FIX_LEFT_QUOTES = re.compile(r"(?<=['\"])\s+")
FIX_RIGHT_QUOTES = re.compile(r"(?<!\w|\d)\s+(?=['\"])", re.UNICODE)
FIX_LEFT_BRACES = re.compile(r"(?<=[\[\(\}])\s+")
FIX_RIGHT_BRACES = re.compile(r"\s+(?=[\]\}\)])")
FIX_SPACES = re.compile(r"\s{2,}")
FIX_QUOTES = re.compile(r"'{2,}")
FIX_SHORT_FORMS = re.compile(r"\s+'(re|s|t)\b", re.IGNORECASE)
FIX_ROMAN_NUMERALS = re.compile(
    r"""
        \b
            M{0,4}
            (CM|CD|D?C{0,3})
            (XC|XL|L?X{0,3})
            (IX|IV|V?I{0,3})
        \b
    """,
    re.VERBOSE | re.IGNORECASE
)


def init(path):
    nltk.data.path.insert(0, path)

    for language in nltk.corpus.stopwords.fileids():
        stopwords_set = frozenset(nltk.corpus.stopwords.words(language))
        stopwords_set = six.moves.map(nltk.wordpunct_tokenize, stopwords_set)
        stopwords_set = itertools.chain.from_iterable(stopwords_set)
        PRECALCULATED_LANGSETS[language] = frozenset(stopwords_set)


def fix_roman_numeral(matcher):
    """
    Uppercases roman numerals. Has to be used with regexp FIX_ROMAN_NUMERALS.
    """

    return matcher.group(0).upper()


def fix_short_form(matcher):
    """
    Fixes short forms like "don 't" or "nobody 's". Has to be used with
    regexp FIX_SHORT_FORMS.
    """

    return "'" + matcher.group(1).lower()


def specific_capitalize(text):
    """
    Capitalize text according to the NLTK.
    """

    if set(text) & CYRILLIC_ALPHABET:
        language = "russian"
    else:
        words = set(nltk.wordpunct_tokenize(text.lower()))
        language = max(
            nltk.corpus.stopwords.fileids(),
            key=lambda lang: len(words & PRECALCULATED_LANGSETS[lang])
        )

    class_ = EnglishCapitalization
    if language == "russian":
        class_ = RussianCapitalization
    elif language == "spanish":
        class_ = SpanishCapitalization
    elif language == "dutch":
        class_ = DutchCapitalization
    return class_().capitalize(text)


def capitalize(text):
    """
    Text capitalizator. Give it a text, it will try to capitalize it according
    to the rules of the language and returns somewhat properly capitalized
    result.
    """

    text = SEPARATORS.sub(r" \1 ", text)

    text = " / ".join(specific_capitalize(part) for part in text.split("/"))

    text = FIX_LEFT_QUOTES.sub("", text)
    text = FIX_RIGHT_QUOTES.sub("", text)
    text = FIX_LEFT_BRACES.sub("", text)
    text = FIX_RIGHT_BRACES.sub("", text)
    text = FIX_SPACES.sub("", text)
    text = FIX_QUOTES.sub('"', text)
    text = FIX_PUNCTUATION.sub("", text)

    text = FIX_SHORT_FORMS.sub(fix_short_form, text)
    text = FIX_ROMAN_NUMERALS.sub(fix_roman_numeral, text)
    text = text.replace(" MIX", " Mix")

    return text.strip()
