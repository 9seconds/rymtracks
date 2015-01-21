# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

import itertools

from .world import WorldCapitalization


class SpanishCapitalization(WorldCapitalization):
    """
    Implementation for Spanish capitalization.
    """

    PREPOSITIONS = (
        "bajo",
        "con",
        "contra",
        "antes de",
        "cerca de",
        "delante de",
        "dentro de",
        "encima de",
        "desde",
        "durante",
        "enfrente de",
        "fuera de",
        "entre",
        "hacia",
        "hasta",
        "para",
        "por",
        "sin",
        "sobre",
        "tras",
        "según",
        "detrás de",
        "después de"
        "en",
        "de",
    )

    PLACE_IDS = (
        "río",
        "lago",
        "monte"
    )

    LANGUAGES = (
        "albano",
        "alemán",
        "andorrano",
        "austriaco",
        "belga",
        "bielorruso",
        "bosnio",
        "búlgaro",
        "checo",
        "croata",
        "danés",
        "eslovaco",
        "esloveno",
        "español",
        "estonio",
        "fines",
        "francés",
        "griego",
        "holandés",
        "húngaro",
        "inglés",
        "irlandés",
        "islandés",
        "italiano",
        "letón",
        "lituano",
        "luxemburgués",
        "macedonio",
        "montenegrino",
        "noruego",
        "polaco",
        "portugués",
        "rumano",
        "ruso",
        "servio",
        "sueco",
        "suizo",
        "ucraniano",
        "argentino",
        "boliviano",
        "brasileño",
        "canadiense",
        "chileno",
        "colombiano",
        "costarricense",
        "cubano",
        "dominicano",
        "ecuatoriano",
        "salvadoreño",
        "guatemalteco",
        "hondureño",
        "mexicano",
        "nicaragüense",
        "panameño",
        "paraguayo",
        "peruani",
        "portorriqueño",
        "estadounidense",
        "uruguayo",
        "venezolanoa",
        "argentino",
        "boliviano",
        "brasileño",
        "canadiense",
        "chileno",
        "colombiano",
        "costarricense",
        "cubano",
        "dominicano",
        "ecuatoriano",
        "salvadoreño",
        "guatemalteco",
        "hondureño",
        "mexicano",
        "nicaragüense",
        "panameño",
        "paraguayo",
        "peruani",
        "portorriqueño",
        "estadounidense",
        "uruguayo",
        "venezolanoa",
    )

    SUBSTITUTIONS = itertools.chain(PREPOSITIONS, PLACE_IDS, LANGUAGES)
    SUBSTITUTIONS = list(SUBSTITUTIONS)

    @classmethod
    def apply_specifics(cls, sentence):
        first, rest = sentence.split(" ", 1)
        for prep in cls.SUBSTITUTIONS:
            rest = rest.replace(prep.capitalize(), prep)
        return " ".join((first, rest))