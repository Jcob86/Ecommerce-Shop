from rest_framework import serializers
from .models import Product, ProductImage, Collection, Promotion


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class ShowCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)
        #  CHECK
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    collection = ShowCollectionSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'size', 'inventory', 'price', 'gender', 'collection', 'images']