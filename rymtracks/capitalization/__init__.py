# -*- coding: utf-8 -*-
"""
This package contains implementations of proper RYM capitalization.

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


from re import compile as regex_compile, IGNORECASE as re_IGNORECASE, \
    VERBOSE as re_VERBOSE, UNICODE as re_UNICODE

from six import PY2, text_type


###############################################################################


__all__ = "capitalize",


###############################################################################


if not PY2:
    from .py3 import capitalize as specific_capitalize
else:
    try:
        from .py2 import capitalize as specific_capitalize
    except LookupError:
        from .py3 import capitalize as specific_capitalize


###############################################################################


FIX_PUNCTUATION = regex_compile(r"\s+(?=[\.,!?:;])")
SEPARATORS = regex_compile(r"([\[\]\(\)'\"\{\}\.,?!:;])")
FIX_LEFT_QUOTES = regex_compile(r"(?<=['\"])\s+")
FIX_RIGHT_QUOTES = regex_compile(r"(?<!\w|\d)\s+(?=['\"])", re_UNICODE)
FIX_LEFT_BRACES = regex_compile(r"(?<=[\[\(\}])\s+")
FIX_RIGHT_BRACES = regex_compile(r"\s+(?=[\]\}\)])")
FIX_SPACES = regex_compile(r"\s{2,}")
FIX_QUOTES = regex_compile(r"'{2,}")
FIX_SHORT_FORMS = regex_compile(r"\s+'(re|s|t)\b", re_IGNORECASE)
FIX_ROMAN_NUMERALS = regex_compile(
    r"""
        \b
            M{0,4}
            (CM|CD|D?C{0,3})
            (XC|XL|L?X{0,3})
            (IX|IV|V?I{0,3})
        \b
    """,
    re_VERBOSE | re_IGNORECASE
)


###############################################################################


def fix_roman_numeral(matcher):
    """
    Uppercases roman numerals. Has to be used with regexp FIX_ROMAN_NUMERALS.
    """
    return matcher.group(0).upper()


def fix_short_form(matcher):
    """
    Fixes short forms like "don 't" or "nobody 's". Has to be used with
    regexp FIX_SHORT_FORMS.
    """
    return "'" + matcher.group(1).lower()


def capitalize(text):
    """
    Text capitalizator. Give it a text, it will try to capitalize it according
    to the rules of the language and returns somewhat properly capitalized
    result.
    """
    text = text_type(text)
    text = SEPARATORS.sub(r" \1 ", text)

    text = " / ".join(specific_capitalize(part) for part in text.split("/"))

    text = FIX_LEFT_QUOTES.sub("", text)
    text = FIX_RIGHT_QUOTES.sub("", text)
    text = FIX_LEFT_BRACES.sub("", text)
    text = FIX_RIGHT_BRACES.sub("", text)
    text = FIX_SPACES.sub("", text)
    text = FIX_QUOTES.sub('"', text)
    text = FIX_PUNCTUATION.sub("", text)

    text = FIX_SHORT_FORMS.sub(fix_short_form, text)
    text = FIX_ROMAN_NUMERALS.sub(fix_roman_numeral, text)
    text = text.replace(" MIX", " Mix")

    return text.strip()
