# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

from .world import WorldCapitalization


class RussianCapitalization(WorldCapitalization):
    """
    Implementation of Russian capitalization.
    """

    @classmethod
    def apply_specifics(cls, sentence):
        return sentence.capitalize()