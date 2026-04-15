from rest_framework import serializers
from .models import (
    Product,
    Attribute,
    AttributeValue,
    ProductAttribute,
    ProductVariant,
    VariantAttribute
)

# =====================================================
# 1. ATTRIBUTE SYSTEM
# =====================================================

class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(
        source='attribute.name',
        read_only=True
    )

    class Meta:
        model = AttributeValue
        fields = [
            'id',
            'attribute_name',
            'value'
        ]


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = [
            'id',
            'name',
            'values'
        ]


# =====================================================
# 2. VARIANT ATTRIBUTE (FLATTENED RESPONSE)
# =====================================================

class VariantAttributeSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(
        source='attribute_value.attribute.name',
        read_only=True
    )
    value = serializers.CharField(
        source='attribute_value.value',
        read_only=True
    )

    class Meta:
        model = VariantAttribute
        fields = [
            'attribute',
            'value'
        ]


# =====================================================
# 3. PRODUCT VARIANT
# =====================================================

class ProductVariantSerializer(serializers.ModelSerializer):
    variant_attributes = VariantAttributeSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'price',
            'stock',
            'image',
            'variant_attributes'
        ]


# =====================================================
# 4. PRODUCT ATTRIBUTE
# =====================================================

class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(
        source='attribute.name',
        read_only=True
    )

    class Meta:
        model = ProductAttribute
        fields = [
            'attribute_name'
        ]


# =====================================================
# 5. PRODUCT LIST SERIALIZER (FAST RESPONSE)
# =====================================================

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'image',
            'is_featured',
            'category'
        ]


# =====================================================
# 6. PRODUCT DETAIL SERIALIZER (FULL DATA)
# =====================================================

class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        source='category.name',
        read_only=True
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    product_attributes = ProductAttributeSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'image',
            'is_featured',
            'category',
            'product_attributes',
            'variants'
        ]


# =====================================================
# 7. PRODUCT QUICK VIEW (FOR HOMEPAGE / POPUPS)
# =====================================================

class ProductQuickViewSerializer(serializers.ModelSerializer):
    first_variant = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'image',
            'first_variant'
        ]

    def get_first_variant(self, obj):
        variant = obj.variants.first()

        if not variant:
            return None

        return {
            "id": variant.id,
            "price": variant.price,
            "stock": variant.stock
        }