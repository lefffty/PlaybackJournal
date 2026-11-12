from enum import IntEnum


class SongConsts(IntEnum):
    NAME_MAX_LENGTH =           128
    LIST_PER_PAGE =             150
    ARTIST_SONG_INLINE_EXTRA =  1


class RatedSongConsts(IntEnum):
    MAX_RATING =        10
    MIN_RATING =        1
    DEFAULT_RATING =    1
