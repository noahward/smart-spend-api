from djoser.serializers import TokenSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenSerializer(TokenSerializer):
    def to_representation(self, instance):
        user_info = {
            "email": instance.user.email,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
        }
        token_info = super().to_representation(instance)
        return {**user_info, **token_info}
