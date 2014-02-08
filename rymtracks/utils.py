# -*- coding: utf-8 -*-
"""
Just a collections ot utilites used here and there.
"""


from six import PY2, text_type as text_type_


###############################################################################


def text_type(text):
    """
    text_type and u from six won't give you good results anytime if you know
    that charset is UTF-8.
    """
    if PY2 and isinstance(text, str):
        return text.decode("utf-8")
    return text_type_(text)
