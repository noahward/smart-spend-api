import codecs
from datetime import datetime

from ofxparse import OfxParser
from requests import Request
from rest_framework import status, generics
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
        if request.data["category"]:
            request.data["date_classified"] = datetime.now()
        return super(TransactionDetail, self).partial_update(request, *args, **kwargs)


@api_view(["POST"])
def preview_transaction_file(request):
    f = request.data["file"]

    with codecs.EncodedFile(f, "utf-8") as fileobj:
        ofx = OfxParser.parse(fileobj)

    response_data = []

    for account in ofx.accounts:
        transaction_list = account.statement.transactions
        account_data = {"kind": account.account_type, "transactions": []}
        for transaction in transaction_list:
            account_data["transactions"].append(
                {
                    "date": transaction.date,
                    "amount": transaction.amount,
                    "description": transaction.payee,
                    "currency_code": account.statement.currency,
                }
            )
        response_data.append(account_data)

    return Response(response_data, status=status.HTTP_200_OK)
