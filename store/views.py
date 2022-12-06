from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, ProductImage, Promotion, Collection
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from .filters import ProductFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    ordering_fields = ['price', 'inventory']

    def get_serializer_context(self):
        return {'request': self.request}