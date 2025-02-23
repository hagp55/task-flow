import factory
import factory.fuzzy
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from src.apps.users.models import User

faker = FakerFactory.create()

EXISTS_GOOGLE_USER_ID = 25
EXISTS_GOOGLE_EMAIL = "test@google.com"


@register(_name="user")
class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    first_name = factory.LazyFunction(lambda: faker.name())
