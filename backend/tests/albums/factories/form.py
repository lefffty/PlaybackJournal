import factory
import base64
import io

from PIL import Image
from faker import Factory
from datetime import datetime

from django.utils import timezone

from albums.constants import AlbumConsts


faker = Factory.create()


def _make_b64_cover(width=200, height=200, color="blue", fmt="JPEG"):
    img = Image.new("RGB", (width, height), color)
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("ascii")


class AlbumCreateDataFactory(factory.DictFactory):
    name = factory.LazyFunction(
        lambda: faker.name()[:AlbumConsts.NAME_MAX_LENGTH]
    )
    publication_date = factory.LazyFunction(lambda: timezone.now().date())
    cover = factory.LazyFunction(_make_b64_cover)
