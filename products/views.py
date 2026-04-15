from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductQuickViewSerializer
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    # =====================================================
    # OPTIMIZED QUERYSET (PERFORMANCE CORE)
    # =====================================================
    def get_queryset(self):
        queryset = Product.objects.all()

        # Optimize DB performance (VERY IMPORTANT)
        queryset = queryset.select_related('category').prefetch_related(
            'variants__variant_attributes__attribute_value__attribute',
            'product_attributes__attribute'
        )

        # SEARCH
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # FILTER: category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # FILTER: featured
        is_featured = self.request.query_params.get('is_featured')
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured)

        return queryset

    # =====================================================
    # DYNAMIC SERIALIZERS
    # =====================================================
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer

        if self.action == 'retrieve':
            return ProductDetailSerializer

        return ProductDetailSerializer

    # =====================================================
    # FEATURED PRODUCTS API
    # =====================================================
    @action(detail=False, methods=['get'])
    def featured(self, request):
        products = self.get_queryset().filter(is_featured=True)

        serializer = ProductListSerializer(products, many=True)

        return Response({
            "count": products.count(),
            "results": serializer.data
        })

    # =====================================================
    # QUICK VIEW API (HOMEPAGE / CARDS)
    # =====================================================
    @action(detail=True, methods=['get'])
    def quick_view(self, request, pk=None):
        product = self.get_object()

        serializer = ProductQuickViewSerializer(product)

        return Response(serializer.data)

    # =====================================================
    # VARIANTS API (VERY IMPORTANT FOR CART SYSTEM)
    # =====================================================
    @action(detail=True, methods=['get'])
    def variants(self, request, pk=None):
        product = self.get_object()

        variants = product.variants.all()

        data = []

        for variant in variants:
            data.append({
                "id": variant.id,
                "price": variant.price,
                "stock": variant.stock,
                "image": request.build_absolute_uri(variant.image.url) if variant.image else None,
                "attributes": [
                    {
                        "attribute": va.attribute_value.attribute.name,
                        "value": va.attribute_value.value
                    }
                    for va in variant.variant_attributes.all()
                ]
            })

        return Response(data)

    # =====================================================
    # SEARCH API (OPTIONAL CLEAN ENDPOINT)
    # =====================================================
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')

        products = self.get_queryset().filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        serializer = ProductListSerializer(products, many=True)

        return Response(serializer.data)