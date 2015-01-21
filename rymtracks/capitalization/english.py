# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

import nltk

from .base import Capitalization


class EnglishCapitalization(Capitalization):
    """
    Implementation of capitalization for English language.
    """

    # POS tags detected by NLTK for the words have to be lowercased.
    # Checkout a list here:
    # http://ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    POS_TAG_LOWER_CASE = {"CC", "IN", "TO"}
    WORD_LOWER_CASE = {"vs.", "v.", "etc", "the", "a", "an", "of"}

    @classmethod
    def generate_trucased_words(cls, tagged_words):
        for word, tag in tagged_words:
            if word == "n't":
                yield word
            elif word in cls.POS_TAG_LOWER_CASE:
                yield word
            elif word in cls.WORD_LOWER_CASE:
                yield word
            elif "-" in word or "." in word:
                yield word.title()
            elif word == "``":
                yield '"'
            else:
                yield word.capitalize()


    @classmethod
    def capitalize_sentence(cls, sentence):
        words = nltk.word_tokenize(sentence)
        tagged_words = nltk.pos_tag([word.lower() for word in words])
        truecased_words = list(cls.generate_trucased_words(tagged_words))

        if truecased_words:
            for idx in (0, -1):
                word = truecased_words[idx]
                if word != word.upper():
                    truecased_words[idx] = word.capitalize()

        return " ".join(truecased_words)