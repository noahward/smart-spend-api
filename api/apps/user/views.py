from knox.models import AuthToken
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.apps.user.permissions import IsOwner

from .serializers import UserSerializer, LoginUserSerializer, CreateUserSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token_instance = AuthToken.objects.create(user)
        return Response(
            {
                "profile": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": {"key": token_instance[1], "expiry": token_instance[0].expiry},
            }
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token_instance = AuthToken.objects.create(user)
        return Response(
            {
                "profile": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": {"key": token_instance[1], "expiry": token_instance[0].expiry},
            }
        )


class MainUser(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
