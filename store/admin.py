from django.contrib import admin
from .models import Collection, Promotion, Product, ProductImage
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet

admin.site.register(Promotion)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
        return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    list_display = ['title', 'price',
                    'inventory', 'size', 'collection_title']
    inlines = [ProductImageInline]
    search_fields = ['title']
    list_filter = ['collection', 'gender']
    list_editable = ['price', 'inventory']

    def collection_title(self, product):
        return product.collection.title


class ProductsCountFilter(admin.SimpleListFilter):
    title = 'products count'
    parameter_name = 'products_count'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'), ('>=10', 'High')
        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(products_count__lt=10)
        elif self.value() == '>=10':
            return queryset.filter(products_count__gte=10)
    

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['product']
    list_display = ['title', 'products_count']
    list_filter = [ProductsCountFilter]
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

    
