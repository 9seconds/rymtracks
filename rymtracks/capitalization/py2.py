# -*- coding: utf-8 -*-
"""
This module contains capitalization definitions for RYM in Python 2.
"""


from .. import NLTK_PATH

from itertools import chain

from nltk import word_tokenize, wordpunct_tokenize, sent_tokenize, pos_tag, \
    data as NLTK_DATA
from nltk.corpus import stopwords
from six import text_type


###############################################################################


# This small hack (?) helps NLTK to find its files.
NLTK_DATA.path[0:0] = [NLTK_PATH]


###############################################################################


PRECALCULATED_LANGSETS = {}
for _language in stopwords.fileids():
    stopwords_set = set(
        text_type(wrd, "utf-8") for wrd in stopwords.words(_language)
    )
    stopwords_set = (wordpunct_tokenize(word) for word in stopwords_set)
    PRECALCULATED_LANGSETS[_language] = set(chain.from_iterable(stopwords_set))

CYRILLIC_ALPHABET = text_type("ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬЬБЮ", "utf-8")
CYRILLIC_ALPHABET = frozenset(CYRILLIC_ALPHABET + CYRILLIC_ALPHABET.lower())


###############################################################################


class Capitalization(object):
    """
    Base capitalization framework class. Inherit to specify the logic.
    """

    def capitalize_sentence(self, sentence):
        """
        Capitalizes particular sentence.
        """
        return " ".join(chunk.capitalize() for chunk in sentence.split())

    def capitalize(self, text):
        """
        Capitalizes whole text.
        """
        return " ".join(
            self.capitalize_sentence(sent) for sent in sent_tokenize(text)
        )


class EnglishCapitalization(Capitalization):
    """
    Implementation of capitalization for English language.
    """

    # POS tags detected by NLTK for the words have to be lowercased.
    # Checkout a list here:
    # http://ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    POS_TAG_LOWER_CASE = {"CC", "IN", "TO"}
    WORD_LOWER_CASE = {"vs.", "v.", "etc", "the", "a", "an", "of"}

    def capitalize_sentence(self, sentence):
        words = word_tokenize(sentence)
        tagged_words = pos_tag([word.lower() for word in words])

        truecased_words = []
        for word, tag in tagged_words:
            it_is_okay = (
                word == "n't" or
                tag in self.POS_TAG_LOWER_CASE or
                word in self.WORD_LOWER_CASE
            )
            if not it_is_okay:
                if "-" in word or "." in word:
                    word = word.title()
                elif word == "``":
                    word = '"'
                else:
                    word = word.capitalize()
            truecased_words.append(word)

        if truecased_words:
            for idx in (0, -1):
                word = truecased_words[idx]
                if word != word.upper():
                    truecased_words[idx] = word.capitalize()

        return " ".join(truecased_words)


class WorldCapitalization(Capitalization):
    """
    Base class for capitalization for non-english languages.
    """

    def apply_specifics(self, sentence):
        """
        Applies language specifics on a sentence.
        """
        return sentence

    def capitalize_sentence(self, sentence):
        sentence = super(WorldCapitalization, self).capitalize_sentence(
            sentence
        )
        return self.apply_specifics(sentence)


class RussianCapitalization(WorldCapitalization):
    """
    Implementation of Russian capitalization.
    """

    def apply_specifics(self, sentence):
        return sentence.capitalize()


class SpanishCapitalization(WorldCapitalization):
    """
    Implementation for Spanish capitalization.
    """

    PREPOSITIONS = (
        "bajo",
        "con",
        "contra",
        "antes de",
        "cerca de",
        "delante de",
        "dentro de",
        "encima de",
        "desde",
        "durante",
        "enfrente de",
        "fuera de",
        "entre",
        "hacia",
        "hasta",
        "para",
        "por",
        "sin",
        "sobre",
        "tras",
        "según",
        "detrás de",
        "después de"
        "en",
        "de",
    )
    PLACE_IDS = (
        "río",
        "lago",
        "monte"
    )
    LANGUAGES = (
        "albano",
        "alemán",
        "andorrano",
        "austriaco",
        "belga",
        "bielorruso",
        "bosnio",
        "búlgaro",
        "checo",
        "croata",
        "danés",
        "eslovaco",
        "esloveno",
        "español",
        "estonio",
        "fines",
        "francés",
        "griego",
        "holandés",
        "húngaro",
        "inglés",
        "irlandés",
        "islandés",
        "italiano",
        "letón",
        "lituano",
        "luxemburgués",
        "macedonio",
        "montenegrino",
        "noruego",
        "polaco",
        "portugués",
        "rumano",
        "ruso",
        "servio",
        "sueco",
        "suizo",
        "ucraniano",
        "argentino",
        "boliviano",
        "brasileño",
        "canadiense",
        "chileno",
        "colombiano",
        "costarricense",
        "cubano",
        "dominicano",
        "ecuatoriano",
        "salvadoreño",
        "guatemalteco",
        "hondureño",
        "mexicano",
        "nicaragüense",
        "panameño",
        "paraguayo",
        "peruani",
        "portorriqueño",
        "estadounidense",
        "uruguayo",
        "venezolanoa",
        "argentino",
        "boliviano",
        "brasileño",
        "canadiense",
        "chileno",
        "colombiano",
        "costarricense",
        "cubano",
        "dominicano",
        "ecuatoriano",
        "salvadoreño",
        "guatemalteco",
        "hondureño",
        "mexicano",
        "nicaragüense",
        "panameño",
        "paraguayo",
        "peruani",
        "portorriqueño",
        "estadounidense",
        "uruguayo",
        "venezolanoa",
    )
    SUBSTITUTIONS = chain(PREPOSITIONS, PLACE_IDS, LANGUAGES)
    SUBSTITUTIONS = [text_type(sbst, "utf-8") for sbst in SUBSTITUTIONS]

    def apply_specifics(self, sentence):
        tokens = sentence.split(" ")
        first, rest = tokens[0], " ".join(tokens[1:])
        for prep in chain(self.SUBSTITUTIONS):
            rest = rest.replace(prep.capitalize(), prep)
        return " ".join([first, rest])


class DutchCapitalization(EnglishCapitalization):
    """
    Implementation of RYM capitalization for Dutch.
    """

    def capitalize_sentence(self, sentence):
        sentence = super(DutchCapitalization, self).capitalize_sentence(
            sentence
        )
        return sentence.replace("Ij", "IJ")


##############################################################################


def capitalize(text):
    """
    Text capitalizator for Python 2.
    """
    if isinstance(text, str):
        text = text.decode("utf-8")
    if set(text) & CYRILLIC_ALPHABET:
        language = "russian"
    else:
        words = set(wordpunct_tokenize(text.lower()))
        language = max(
            stopwords.fileids(),
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
