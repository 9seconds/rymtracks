# -*- coding: utf-8 -*-
"""
Collection of mixins to test RYMTracks.
"""


from rymtracks.core import execute


##############################################################################


class FetchMixin(object):
    """
    Implements simple fetch test case
    """

    def test_fetch(self):
        results = execute([self.URL])
        result = results[0]

        self.assertIsNone(result.exception)
        self.assertEqual(self.DATA, result.data)
