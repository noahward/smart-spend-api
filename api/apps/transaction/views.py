from rest_framework import generics
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from api.apps.account.models import Account

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionList(generics.ListCreateAPIView):
    model = Transaction
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        account = Account.objects.get(id=self.kwargs.get("aid"))
        return Transaction.objects.filter(Q(user=user) & Q(account=account))


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
