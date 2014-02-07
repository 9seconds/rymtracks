# -*- coding: utf-8 -*-


def capitalize(text):
    if "/" in text:
        return " / ".join(capitalize(sent) for sent in text.split("/"))
    else:
        return text.title()