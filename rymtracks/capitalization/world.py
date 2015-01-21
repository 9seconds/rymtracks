# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

from .base import Capitalization


class WorldCapitalization(Capitalization):
    """
    Base class for capitalization for non-english languages.
    """

    @classmethod
    def apply_specifics(cls, sentence):
        """
        Applies language specifics on a sentence.
        """
        return sentence

    @classmethod
    def capitalize_sentence(cls, sentence):
        sentence = Capitalization.capitalize_sentence(sentence)
        return cls.apply_specifics(sentence)