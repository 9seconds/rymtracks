# -*- coding: utf-8 -*-


from itertools import chain
from re import compile as regex_compile

from nltk import wordpunct_tokenize, sent_tokenize, pos_tag
from nltk.corpus import stopwords
from six import PY2, text_type


##############################################################################


CAPITALIZATION_TYPE_RUSSIAN = "russian"
CAPITALIZATION_TYPE_ENGLISH = "english"
CAPITALIZATION_TYPE_LATIN = "latin"

PRECALCULATED_LANGSETS = {}
for language in stopwords.fileids():
    stopwords_set = set()
    for word in stopwords.words(language):
        if PY2:
            word = word.decode("utf-8")
        stopwords_set.add(word)
    stopwords_set = (wordpunct_tokenize(word) for word in stopwords_set)
    PRECALCULATED_LANGSETS[language] = set(chain.from_iterable(stopwords_set))


##############################################################################


class Capitalization(object):

    def capitalize_sentence(self, sentence):
        return " ".join(chunk.capitalize() for chunk in sentence.split())

    def capitalize(self, text):
        text = text_type(text)
        return " ".join(
            self.capitalize_sentence(sent) for sent in sent_tokenize(text)
        )


class EnglishCapitalization(Capitalization):

    VERSUS = {"vs.", "v."}
    ETC = {"etc"}

    POS_TAG_LOWER_CASE = {"CC", "IN", "TO"}
    WORD_LOWER_CASE = {"vs.", "v.", "etc", "the"}

    FIX_PUNCTUATION = regex_compile(r" (?=[\.,'!?:;])")

    def capitalize_sentence(self, sentence):
        sentence = sentence.replace("'n'", " 'n' ")

        words = wordpunct_tokenize(sentence)
        tagged_words = pos_tag([word.lower() for word in words])

        truecased_words = []
        is_first = True
        for word, tag in tagged_words:
            if word == "n't" and not is_first:
                truecased_words[-1] += word
                continue
            elif tag in self.POS_TAG_LOWER_CASE or word in self.WORD_LOWER_CASE:
                pass
            elif "-" in word or "." in word:
                word = word.title()
            elif word == "``":
                word = '"'
            else:
                word = word.capitalize()
            truecased_words.append(word)
            is_first = False

        for idx in (0, -1):
            word = truecased_words[idx][0]
            if word != word.upper():
                truecased_words[idx][0] = word.capitalize()

        coerced_sentence = " ".join(truecased_words)
        coerced_sentence = coerced_sentence.replace("'n '", "'n'")
        coerced_sentence = self.FIX_PUNCTUATION.sub("", coerced_sentence)

        return coerced_sentence


##############################################################################


def capitalize(text):
    words = set(wordpunct_tokenize(text_type(text).lower()))
    language = max(
        stopwords.fileids(),
        key=lambda lang: len(words & PRECALCULATED_LANGSETS[lang])
    )

    if language in ("portuguese", "spanish"):
        return EnglishCapitalization().capitalize(text)
    if language == "russian":
        return Capitalization().capitalize(text)
    return Capitalization().capitalize(text)
