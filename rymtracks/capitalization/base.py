# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

import nltk
import six


class Capitalization(object):
    """
    Base capitalization framework class. Inherit to specify the logic.
    """

    @classmethod
    def capitalize_sentence(cls, sentence):
        """
        Capitalizes particular sentence.
        """

        return " ".join(chunk.capitalize() for chunk in sentence.split())

    @classmethod
    def capitalize(cls, text):
        """
        Capitalizes whole text.
        """

        sentences = six.moves.map(cls.capitalize_sentence, nltk.sent_tokenize(text))
        return " ".join(sentences)