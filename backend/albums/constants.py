from enum import IntEnum


class AlbumConsts(IntEnum):
    NAME_MAX_LENGTH =       128
    SONG_INLINE_EXTRA =     5
    GENRE_INLINE_EXTRA =    1
    ARTIST_INLINE_EXTRA =   1
    PAGINATION_PAGE_SIZE =  15


class RatedAlbumConsts(IntEnum):
    MIN_RATING =        1
    MAX_RATING =        10
    DEFAULT_RATING =    1
