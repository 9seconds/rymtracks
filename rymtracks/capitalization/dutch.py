# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

from .english import EnglishCapitalization


class DutchCapitalization(EnglishCapitalization):
    """
    Implementation of RYM capitalization for Dutch.
    """

    @classmethod
    def capitalize_sentence(cls, sentence):
        sentence = EnglishCapitalization.capitalize_sentence(sentence)
        return sentence.replace("Ij", "IJ")