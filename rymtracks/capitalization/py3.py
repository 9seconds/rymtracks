# -*- coding: utf-8 -*-


def capitalize(text):
    if "/" in text:
        return text.replace("/", " / ")
    return text
