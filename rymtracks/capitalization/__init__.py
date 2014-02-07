# -*- coding: utf-8 -*-
"""
This package contains implementation of proper RYM capitalization.

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


from re import compile as regex_compile

from six import PY2


###############################################################################


__all__ = "capitalize",


###############################################################################


if PY2:
    from .py2 import capitalize as specific_capitalize
else:
    from .py3 import capitalize as specific_capitalize


###############################################################################


FIX_PUNCTUATION = regex_compile(r"\s+(?=[\.,'!?:;])")
FIX_SPACES = regex_compile(r"\s{2,}")


###############################################################################


def capitalize(text):
    """
    Text capitalizator. Give it a text, it will try to capitalize it according
    to the rules of the language and returns somewhat properly capitalized
    result.
    """
    text = specific_capitalize(text)
    text = FIX_PUNCTUATION.sub("", text)
    text = FIX_SPACES.sub("", text)
    return text.strip()
