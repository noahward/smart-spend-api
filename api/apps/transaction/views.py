from datetime import datetime

import pandas as pd
from requests import Request
from pandera.errors import SchemaError
from rest_framework import generics
from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from api.apps.account.models import Account

from .models import Transaction
from .df_helpers import validate_df
from .serializers import TransactionSerializer


class TransactionList(generics.ListCreateAPIView):
    model = Transaction
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        account = Account.objects.get(id=self.kwargs.get("aid"))
        return Transaction.objects.filter(Q(user=user) & Q(account=account))

    # TODO: Don't hardcode currency
    def post(self, request, *args, **kwargs):
        if "file" in request.data:
            df = pd.read_csv(request.data["file"], header=None)

            try:
                df = df.pipe(validate_df)
            except (pd.errors.OutOfBoundsDatetime, SchemaError):
                raise APIException(
                    "Only unaltered TD statements are accepted at this time"
                )

            df["currency_code"] = "CAD"
            df["account"] = self.kwargs.get("aid")
            df["amount"] = df["deposit"] - df["withdrawal"]
            df["user"] = self.request.user.id
            df["date"] = df["date"].dt.date
            df = df.drop(columns=["withdrawal", "deposit", "new_balance"])

            transaction_list = df.to_dict(orient="records")
            transaction_req = Request(data=transaction_list)

        else:
            transaction = request.data
            transaction["currency_code"] = "CAD"
            transaction["description"] = "manual_balance_update"
            transaction["account"] = self.kwargs.get("aid")
            transaction["date"] = datetime.today().strftime("%Y-%m-%d")
            transaction["user"] = self.request.user.id

            transaction_req = Request(data=transaction)

        return super(TransactionList, self).post(transaction_req, *args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(TransactionList, self).get_serializer(*args, **kwargs)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
