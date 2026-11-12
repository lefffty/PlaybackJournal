import factory
import base64
import io
from faker import Factory
from PIL import Image

from playlist.constants import PlaylistsConsts

faker = Factory.create()


def _make_b64_cover(width=200, height=200, color="blue", fmt="JPEG"):
    img = Image.new("RGB", (width, height), color)
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("ascii")


class PlaylistDataFactory(factory.DictFactory):
    name = factory.LazyFunction(lambda: faker.name()[:PlaylistsConsts.NAME_MAX_LENGTH])
    description = factory.LazyFunction(lambda: faker.sentence()[:PlaylistsConsts.DESCRIPTION_MAX_LENGTH])
    cover = factory.LazyFunction(_make_b64_cover)


class RatedPlaylistDataFactory(factory.DictFactory):
    rating = 3
