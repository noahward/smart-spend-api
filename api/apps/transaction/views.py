from datetime import datetime

from requests import Request
from rest_framework import generics
from django.utils.dateparse import parse_date
from rest_framework.permissions import IsAuthenticated

from api.apps.user.permissions import IsOwner

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionList(generics.ListCreateAPIView):
    model = Transaction
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

    # TODO: Don't hardcode currency
    # TODO: Handle file uploads
    def post(self, request, *args, **kwargs):
        transaction = request.data
        transaction["currency_code"] = "CAD"
        transaction["date"] = parse_date(transaction["date"])
        transaction["user"] = self.request.user.id

        transaction_req = Request(data=transaction)

        return super(TransactionList, self).post(transaction_req, *args, **kwargs)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Transaction
    lookup_url_kwarg = "tid"
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Transaction.objects.filter(id=self.kwargs.get("tid"))

    def patch(self, request, *args, **kwargs):
        request.data["date_classified"] = datetime.now()
        return super(TransactionDetail, self).partial_update(request, *args, **kwargs)
