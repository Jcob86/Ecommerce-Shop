from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, ProductImage, Promotion, Collection
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, CollectionSerializer
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


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']):
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)