# -*- coding: utf-8 -*-


from .. import NLTK_PATH
from ..utils import text_type

from itertools import chain
from re import compile as regex_compile

from nltk import wordpunct_tokenize, sent_tokenize, pos_tag, \
    data as NLTK_DATA
from nltk.corpus import stopwords


###############################################################################


NLTK_DATA.path[0:0] = [NLTK_PATH]


###############################################################################


PRECALCULATED_LANGSETS = {}
for _language in stopwords.fileids():
    stopwords_set = set(text_type(wrd) for wrd in stopwords.words(_language))
    stopwords_set = (wordpunct_tokenize(word) for word in stopwords_set)
    PRECALCULATED_LANGSETS[_language] = set(chain.from_iterable(stopwords_set))

CYRILLIC_ALPHABET = text_type("ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬЬБЮ")
CYRILLIC_ALPHABET = frozenset(CYRILLIC_ALPHABET + CYRILLIC_ALPHABET.lower())


###############################################################################


class Capitalization(object):

    def capitalize_sentence(self, sentence):
        sentence = sentence.replace("'n'", " 'n' ")
        if "/" in sentence:
            tokens = sentence.split("/")
            tokens = [self.capitalize_sentence(tkn) for tkn in tokens]
            sentence = " / ".join(tokens)
        sentence = sentence.replace(" 'n' ", "'n'")
        return " ".join(chunk.capitalize() for chunk in sentence.split())

    def capitalize(self, text):
        text = text_type(text)
        return " ".join(
            self.capitalize_sentence(sent) for sent in sent_tokenize(text)
        )


class EnglishCapitalization(Capitalization):

    POS_TAG_LOWER_CASE = {"CC", "IN", "TO"}
    WORD_LOWER_CASE = {"vs.", "v.", "etc", "the"}

    FIX_NT = regex_compile(r"\s+n't")

    def capitalize_sentence(self, sentence):
        words = wordpunct_tokenize(sentence)
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

        for idx in (0, -1):
            word = truecased_words[idx][0]
            if word != word.upper():
                truecased_words[idx][0] = word.capitalize()

        coerced_sentence = " ".join(truecased_words)
        coerced_sentence = self.FIX_NT.sub("n't", coerced_sentence)

        return coerced_sentence


class WorldCapitalization(Capitalization):

    def apply_specifics(self, sentence):
        return sentence

    def capitalize_sentence(self, sentence):
        sentence = super(WorldCapitalization, self).capitalize_sentence(
            sentence
        )
        return self.apply_specifics(sentence)


class RussianCapitalization(WorldCapitalization):

    def apply_specifics(self, sentence):
        return sentence.capitalize()


class SpanishCapitalization(WorldCapitalization):

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
    SUBSTITUTIONS = [text_type(sbst) for sbst in SUBSTITUTIONS]

    def apply_specifics(self, sentence):
        tokens = sentence.split(" ")
        first, rest = tokens[0], " ".join(tokens[1:])
        for prep in chain(self.SUBSTITUTIONS):
            rest = rest.replace(prep.capitalize(), prep)
        sentence = " ".join([first, rest])


##############################################################################


def capitalize(text):
    if set(text) & set(CYRILLIC_ALPHABET):
        language = "russian"
    else:
        words = set(wordpunct_tokenize(text_type(text).lower()))
        language = max(
            stopwords.fileids(),
            key=lambda lang: len(words & PRECALCULATED_LANGSETS[lang])
        )

    class_ = EnglishCapitalization
    if language == "russian":
        class_ = RussianCapitalization
    elif language == "spanish":
        class_ = SpanishCapitalization
    return class_().capitalize(text)
