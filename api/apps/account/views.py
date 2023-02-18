from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.apps.user.permissions import IsOwner

from .models import Account
from .serializers import AccountSerializer


class AccountList(generics.ListCreateAPIView):
    model = Account
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsOwner]
