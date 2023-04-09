import json
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
from .helpers import process_transaction_file
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


class TransactionFileUpload(generics.CreateAPIView):
    model = Transaction
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(TransactionFileUpload, self).get_serializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        transaction_file = request.FILES["file"]
        account_map = json.loads(request.POST["map"])

        with codecs.EncodedFile(transaction_file, "utf-8") as fileobj:
            ofx = OfxParser.parse(fileobj)

        transaction_data = process_transaction_file(ofx, account_map, request.user.id)

        transaction_list = []
        for account in transaction_data:
            transaction_list.extend(account["transactions"])

        transaction_req = Request(data=transaction_list)

        return super(TransactionFileUpload, self).post(transaction_req, *args, **kwargs)


@api_view(["POST"])
def preview_transaction_file(request):
    transaction_file = request.data["file"]

    with codecs.EncodedFile(transaction_file, "utf-8") as fileobj:
        ofx = OfxParser.parse(fileobj)

    response_data = process_transaction_file(ofx)

    return Response(response_data, status=status.HTTP_200_OK)
