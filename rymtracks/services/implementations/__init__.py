# -*- coding: utf-8 -*-


from .allmusic import AllMusic
from .amazon import Amazon
from .archiveorg import ArchiveOrg
from .bandcamp import BandCamp
from .beatport import BeatPort
from .boomkat import Boomkat
from .discogs import Discogs
from .filesystem import FileSystem
from .freemusicarchive import FreeMusicArchive
from .itunes import ITunes
from .jamendo import Jamendo
from .junodownload import JunoDownload
from .lastfm import LastFM
from .musicbrainz import MusicBrainz
from .progarchives import ProgArchives
from .rateyourmusic import RateYourMusic
from .sevendigital import SevenDigital
from ..base import Service


###############################################################################


FILESYSTEM_LOCATION = "*"


###############################################################################


Service.register(AllMusic, "allmusic.com")
Service.register(Amazon, "amazon.com", "amazon.co.uk", "amazon.co.jp")
Service.register(ArchiveOrg, "archive.org")
Service.register(BandCamp, "bandcamp.com")
Service.register(BeatPort, "beatport.com")
Service.register(Boomkat, "boomkat.com")
Service.register(Discogs, "discogs.com")
Service.register(
    FreeMusicArchive,
    "freemusicarchive.org", "freemusicarchive.com"
)
Service.register(ITunes, "itunes.apple.com")
Service.register(Jamendo, "jamendo.com")
Service.register(JunoDownload, "junodownload.com")
Service.register(
    LastFM,
    "last.fm", "lastfm.ru", "lastfm.de", "lastfm.es", "lastfm.fr",
    "lastfm.it", "lastfm.jp", "lastfm.pl", "lasfm.com.br", "lastfm.se",
    "lastfm.com.tr", "cn.last.fm"
)
Service.register(MusicBrainz, "musicbrainz.org")
Service.register(ProgArchives, "progarchives.com")
Service.register(RateYourMusic, "rateyourmusic.com")
Service.register(SevenDigital, "7digital.com")
Service.register(FileSystem, FILESYSTEM_LOCATION)
