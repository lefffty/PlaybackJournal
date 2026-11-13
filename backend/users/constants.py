from enum import IntEnum


class UsersConsts(IntEnum):
    NAME_MAX_LENGTH =       64
    SURNAME_MAX_LENGTH =    64
    USERNAME_MAX_LENGTH =   64

    LISTENED_ALBUM_INLINE_EXTRA =   1
    RATED_ALBUM_INLINE_EXTRA =      1
    FAVOURITE_ALBUM_INLINE_EXTRA =  1


class SearchConsts(IntEnum):
    LIMIT = 10
