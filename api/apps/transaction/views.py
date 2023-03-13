import pandas as pd
from requests import Request
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

    # TODO: Pydantic for dataframe validation
    def post(self, request, *args, **kwargs):
        df = pd.read_csv(
            request.data["file"],
            header=None,
            names=["date", "description", "withdrawal", "deposit", "new_balance"],
        )
        df[["withdrawal", "deposit"]] = df[["withdrawal", "deposit"]].fillna(value=0)
        df["currency_code"] = "CAD"
        df["account"] = Account.objects.get(id=self.kwargs.get("aid"))
        df["amount"] = df["deposit"] - df["withdrawal"]
        df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
        df["user"] = self.request.user
        df = df.drop(columns=["withdrawal", "deposit", "new_balance"])

        transaction_list = df.to_dict(orient="records")
        transaction_req = Request(data=transaction_list)
        return super(TransactionList, self).post(transaction_req, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(TransactionList, self).get_serializer(*args, **kwargs)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
