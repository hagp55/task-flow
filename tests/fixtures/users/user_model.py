import factory
import factory.fuzzy
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from src.apps.users.models import User

faker = FakerFactory.create()


@register(_name="user")
class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    first_name = factory.LazyFunction(lambda: faker.name())
    google_access_token = factory.LazyFunction(lambda: faker.sha256())
    yandex_access_token = factory.LazyFunction(lambda: faker.sha256())
