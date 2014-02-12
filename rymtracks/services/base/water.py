# -*- coding: utf-8 -*-


from six import PY2, Iterator, text_type, callable as six_callable, \
    string_types


###############################################################################


__all__ = "Water",


###############################################################################


class Water(Iterator):
    """
    Just simple wrapper around BeautifulSoup to avoid "if"-mess.
    """

    __slots__ = "_soup",

    # ------------------------------------------------------------------------

    def __init__(self, soup):
        self._soup = soup

    def __nonzero__(self):
        return bool(self._soup) if self._soup else False

    def __instancecheck__(self, instance):
        return isinstance(instance, getattr(self._soup, "__class__", None))

    def __len__(self):
        return len(self._soup) if self._soup else 0

    def __getitem__(self, key):
        return Water(self._soup[key]) if self._soup else self

    def __setitem__(self, key, value):
        if self._soup:
            self._soup[key] = value

    def __delitem__(self, key):
        if self._soup:
            del self._soup[key]

    def __iter__(self):
        return Water(iter(self._soup)) if self._soup else iter([])

    def __contains__(self, key):
        return key in self._soup if self._soup else False

    def __getslice__(self, i, j):
        return Water(self._soup[i:j]) if self._soup else Water([])

    def __getattr__(self, item):
        if hasattr(self._soup, item):
            return Water(getattr(self._soup, item))
        return self

    def __call__(self, *args, **kwargs):
        if six_callable(self._soup):
            return Water(self._soup(*args, **kwargs))
        return self

    def __str__(self):
        if self._soup:
            text = self._soup
            if not isinstance(self._soup, string_types):
                text = self._soup.get_text()
            return text_type(text.strip())
        else:
            return text_type("")

    if PY2:
        def __unicode__(self):
            return self.__str__()

    def __repr__(self):
        return repr(self._soup)

    def __next__(self):
        return Water(next(self._soup))