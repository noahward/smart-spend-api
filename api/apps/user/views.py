from djoser import utils, signals
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        kwargs["data"] = {"uid": self.kwargs["uid"], "token": self.kwargs["token"]}

        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data_with_token = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            user_data_with_token, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        token = utils.login_user(self.request, user)
        token_serializer = settings.SERIALIZERS.token
        return token_serializer(token).data
