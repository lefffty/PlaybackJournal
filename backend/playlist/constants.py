from enum import IntEnum


class PlaylistsConsts(IntEnum):
    NAME_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 512
    SONG_INLINE_EXTRA = 1


class RatedPlaylistsConsts(IntEnum):
    MIN_RATING = 1
    MAX_RATING = 10
    DEFAULT_RATING = 1
