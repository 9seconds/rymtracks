# -*- coding: utf-8 -*-


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
    text = specific_capitalize(text)
    text = FIX_PUNCTUATION.sub("", text)
    text = FIX_SPACES.sub("", text)
    return text.strip()
