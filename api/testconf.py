import factory

from api.apps.user.models import User
from api.apps.account.models import Account
from api.apps.category.models import Category

USER_PASSWORD = "password"


class UserFactory(factory.django.DjangoModelFactory):
    password = factory.PostGenerationMethodCall("set_password", USER_PASSWORD)
    email = factory.Sequence("testuser{}@company.com".format)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_superuser = False
    is_staff = False

    class Meta:
        model = User


class AccountFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=2)
    initial_balance = 100
    kind = "saving"
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Account


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=2)
    detailed_name = factory.Faker("sentence", nb_words=3)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Category
