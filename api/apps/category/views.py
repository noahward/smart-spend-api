from rest_framework import generics
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from .models import Category
from .serializers import CategorySerializer


class CategoryList(generics.ListCreateAPIView):
    model = Category
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(Q(user__isnull=True) | Q(user=user))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
