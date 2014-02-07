# -*- coding: utf-8 -*-


from itertools import chain
from re import compile as regex_compile

from nltk import wordpunct_tokenize, sent_tokenize, pos_tag
from nltk.corpus import stopwords
from six import PY2, text_type


##############################################################################


PRECALCULATED_LANGSETS = {}
for language in stopwords.fileids():
    stopwords_set = set()
    for word in stopwords.words(language):
        if PY2:
            word = word.decode("utf-8")
        stopwords_set.add(word)
    stopwords_set = (wordpunct_tokenize(word) for word in stopwords_set)
    PRECALCULATED_LANGSETS[language] = set(chain.from_iterable(stopwords_set))


CYRILLIC_ALPHABET = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬЬБЮ"
if PY2:
    CYRILLIC_ALPHABET = CYRILLIC_ALPHABET.decode("utf-8")
CYRILLIC_ALPHABET = frozenset(CYRILLIC_ALPHABET + CYRILLIC_ALPHABET.lower())


##############################################################################


class Capitalization(object):

    FIX_MULTIPLE_SPACES = regex_compile(r"\s{2,}")

    def capitalize_sentence(self, sentence):
        sentence = sentence.replace("'n'", " 'n' ")
        if sentence.count("/") > 1:
            tokens = sentence.split("/")
            tokens = [self.capitalize_sentence(tkn) for tkn in tokens]
            sentence = " / ".join(tokens)
        sentence = self.FIX_MULTIPLE_SPACES.sub(" ", sentence)
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

    FIX_PUNCTUATION = regex_compile(r" (?=[\.,'!?:;])")
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
        coerced_sentence = self.FIX_PUNCTUATION.sub("", coerced_sentence)
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
        "albano"
        "alemán"
        "andorrano"
        "austriaco"
        "belga"
        "bielorruso"
        "bosnio"
        "búlgaro"
        "checo"
        "croata"
        "danés"
        "eslovaco"
        "esloveno"
        "español"
        "estonio"
        "fines"
        "francés"
        "griego"
        "holandés"
        "húngaro"
        "inglés"
        "irlandés"
        "islandés"
        "italiano"
        "letón"
        "lituano"
        "luxemburgués"
        "macedonio"
        "montenegrino"
        "noruego"
        "polaco"
        "portugués"
        "rumano"
        "ruso"
        "servio"
        "sueco"
        "suizo"
        "ucraniano"
        "argentino"
        "boliviano"
        "brasileño"
        "canadiense"
        "chileno"
        "colombiano"
        "costarricense"
        "cubano"
        "dominicano"
        "ecuatoriano"
        "salvadoreño"
        "guatemalteco"
        "hondureño"
        "mexicano"
        "nicaragüense"
        "panameño"
        "paraguayo"
        "peruani"
        "portorriqueño"
        "estadounidense"
        "uruguayo"
        "venezolanoa"
        "argentino"
        "boliviano"
        "brasileño"
        "canadiense"
        "chileno"
        "colombiano"
        "costarricense"
        "cubano"
        "dominicano"
        "ecuatoriano"
        "salvadoreño"
        "guatemalteco"
        "hondureño"
        "mexicano"
        "nicaragüense"
        "panameño"
        "paraguayo"
        "peruani"
        "portorriqueño"
        "estadounidense"
        "uruguayo"
        "venezolanoa"
    )
    COUNTRIES = (
        "albana"
        "alemana"
        "andorrana"
        "austriaca"
        "bielorrusa"
        "bosnia"
        "búlgara"
        "checa"
        "danesa"
        "eslovaca"
        "eslovena"
        "española"
        "estonia"
        "finesa"
        "francesa"
        "griega"
        "holandesa"
        "húngara"
        "inglesa"
        "irlandesa"
        "islandesa"
        "italiana"
        "letona"
        "lituana"
        "luxemburguesa"
        "macedonia"
        "montenegrina"
        "noruega"
        "polaca"
        "portuguesa"
        "rumana"
        "rusa"
        "servia"
        "sueca"
        "suiza"
        "ucraniana"
        "argentina"
        "boliviana"
        "brasileña"
        "chilena"
        "colombiana"
        "cubana"
        "dominicana"
        "ecuatoriana"
        "salvadoreña"
        "guatemalteca"
        "hondureña"
        "mexicana"
        "panameña"
        "paraguaya"
        "peruana"
        "portorriqueña"
        "uraguayo"
        "argentina"
        "boliviana"
        "brasileña"
        "chilena"
        "colombiana"
        "cubana"
        "dominicana"
        "ecuatoriana"
        "salvadoreña"
        "guatemalteca"
        "hondureña"
        "mexicana"
        "panameña"
        "paraguaya"
        "peruana"
        "portorriqueña"
        "uraguayo"
    )
    SUBSTITUTIONS = (PREPOSITIONS, PLACE_IDS, LANGUAGES, COUNTRIES)

    def apply_specifics(self, sentence):
        tokens = sentence.split(" ")
        first, rest = tokens[0], " ".join(tokens[1:])
        for prep in chain(self.SUBSTITUTIONS):
            if PY2:
                prep = prep.decode("utf-8")
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

    if language == "russian":
        class_ = RussianCapitalization
    elif language == "spanish":
        class_ = SpanishCapitalization
    else:
        class_ = EnglishCapitalization
    return class_().capitalize(text)