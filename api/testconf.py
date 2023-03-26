import factory

from api.apps.user.models import User

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
