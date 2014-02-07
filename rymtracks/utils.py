# -*- coding: utf-8 -*-


from six import PY2, text_type as text_type_


###############################################################################


def text_type(text):
    if PY2 and not isinstance(text, unicode):
        return text.decode("utf-8")
    return text_type_(text)