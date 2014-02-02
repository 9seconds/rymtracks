rymtracks
=========

|Build Status| |PyPi Package|

RYMTracks is small helper for all those folks who actively uses and
contributes for `RateYourMusic <http://rateyourmusic.com>`__.

Unfortunately `sharifi <http://rateyourmusic.com/~sharifi>`__ still has
this unconvenient track list editor you have to fill by yourself. For
big albums you have to copy/paste every song title and print timestamps
in correct form. Moreover, you even have to put track numbers (just a
minute, it is 2014 ongoing) manually.

It is really irritating. Just imagine big albums like `Fantasma
Parastasie <http://www.discogs.com/Aidan-Baker-And-Tim-Hecker-Fantasma-Parastasie/master/5679>`__,
it is really painful: you fill all the data feeling yourself like an
idiot. If you feel my pain, this small tool is for you.

Install
-------

Usage is pretty simple. Your install it from PyPi

::

    $ pip install rymtracks

or like any other Python package

::

    $ git clone https://github.com/9seconds/rymtracks.git
    $ cd rymtracks
    $ ./setup.py install

And here you are, you have small program called ``rymtracks`` in your
``$PATH``!

Usage
-----

Usage is clean and straightforward. In 99% cases you need just a
following

::

    $ rymtracks "http://aidanbaker.bandcamp.com/album/fantasma-parastasie"
    1|Phantom On A Pedestal|5:50
    2|Hymn To The Idea Of Night|5:19
    3|Auditory Spirits|3:44
    4|Skeleton Dance|3:02
    5|Gallery Of The Invisible Woman|7:18
    6|Dream Of The Nightmare|4:20
    7|Fantasma Parastasie|4:50

Here it is! Copypasteable output for RYM advanced tracklist form!
Actually you may put several URLs here to get following

::

    $ rymtracks "http://aidanbaker.bandcamp.com/album/fantasma-parastasie" "http://aidanbaker.bandcamp.com/album/cameo"
    http://aidanbaker.bandcamp.com/album/cameo =====================================
    1|Cameo 1|21:00
    2|Cameo Interlude|8:46
    3|Cameo 2|18:56

    http://aidanbaker.bandcamp.com/album/fantasma-parastasie =======================
    1|Phantom On A Pedestal|5:50
    2|Hymn To The Idea Of Night|5:19
    3|Auditory Spirits|3:44
    4|Skeleton Dance|3:02
    5|Gallery Of The Invisible Woman|7:18
    6|Dream Of The Nightmare|4:20
    7|Fantasma Parastasie|4:50

Sweet, right? RYMTracks supports reading from a file with ``-f`` option
and listing of known network locations it can parse.

::

    $ rymtracks -l
    allmusic.com
    amazon.co.jp
    amazon.co.uk
    amazon.com
    bandcamp.com
    discogs.com
    itunes.apple.com
    musicbrainz.org
    rateyourmusic.com

This covers all my needs but if you want to have some more, just put
request into issues. One notice: I do not want to parse JS-based script
and install Selenium as dependencies. Yeah, I know that WWW goes from
good old plain HTML but seriously, it is really painful. Probably we
need for SoundCloud and I can add it but you have to have your own API
key then, otherwise RYMTracks would be banned there in a few moments.

Cheers.

.. |Build Status| image:: https://travis-ci.org/9seconds/rymtracks.png?branch=master
   :target: https://travis-ci.org/9seconds/rymtracks

.. |PyPi Package| image:: https://badge.fury.io/py/RYMTracks.png
   :target: http://badge.fury.io/py/RYMTracks
