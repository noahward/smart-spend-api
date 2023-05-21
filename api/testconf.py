import random
import datetime

import factory

from api.apps.user.models import User
from api.apps.account.models import Account
from api.apps.category.models import Category
from api.apps.transaction.models import Transaction

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
    currency_code = factory.Iterator(["USD", "CAD", "MXN"])
    initial_balance = 100
    kind = "saving"
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Account


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("sentence", nb_words=2)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Category


class TransactionFactory(factory.django.DjangoModelFactory):
    date = factory.LazyFunction(datetime.date.today)
    description = factory.Faker("catch_phrase")
    currency_code = factory.Iterator(["USD", "CAD", "MXN"])
    amount = round(random.uniform(-1_000_000_000.00, 1_000_000_000.00), 2)
    user = factory.SubFactory(UserFactory)
    account = factory.SubFactory(AccountFactory)

    class Meta:
        model = Transaction
