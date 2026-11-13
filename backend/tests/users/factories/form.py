from django.contrib.auth import get_user_model

import factory
from faker import Factory

from users.constants import UsersConsts


faker = Factory.create()
User = get_user_model()


class UserCreateDataFactory(factory.DictFactory):
    username = factory.LazyFunction(lambda: faker.user_name()[:UsersConsts.USERNAME_MAX_LENGTH])
    last_name = factory.LazyFunction(lambda: faker.last_name()[:UsersConsts.SURNAME_MAX_LENGTH])
    first_name = factory.LazyFunction(lambda: faker.first_name()[:UsersConsts.NAME_MAX_LENGTH])
    email = factory.LazyFunction(lambda: faker.email())
    password = factory.LazyFunction(lambda: faker.password())


class AvatarDataFactory(factory.DictFactory):
    avatar = factory.django.ImageField(
        filename="test_image.jpg", width=200, height=200, color="blue", format="JPEG",
    )


class NewPasswordDataFactory(factory.DictFactory):
    current_password = None
    new_password = "administrator_01"


class SearchDataFactory(factory.DictFactory):
    query = factory.LazyFunction(lambda: faker.text())
