from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer
from .utils import get_or_create_session


class CartViewSet(ViewSet):

    # 🔑 Get or create cart (user or guest)
    def get_cart(self, request):
        if request.user.is_authenticated:
            
            cart, _ = Cart.objects.get_or_create(
                user=request.user,
                session_id=None
            )
        else:
            session_id = get_or_create_session(request)
            cart, _ = Cart.objects.get_or_create(
                session_id=session_id,
                user=None
            )
        return cart

    # 🧾 GET /cart/
    def list(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # ➕ POST /cart/
    def create(self, request):
        cart = self.get_cart(request)

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        # ✅ Validation
        if not product_id:
            return Response(
                {"error": "product_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except ValueError:
            return Response(
                {"error": "Quantity must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Create or update cart item
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                "price": product.price,
                "quantity": quantity
            }
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response(
            {"message": "Item added to cart"},
            status=status.HTTP_200_OK
        )

    # 🔁 PATCH /cart/{item_id}/
    def partial_update(self, request, pk=None):
        cart = self.get_cart(request)

        try:
            item = CartItem.objects.get(id=pk, cart=cart)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get("quantity", 1)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response(
                {"error": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity <= 0:
            item.delete()
            return Response(
                {"message": "Item removed"},
                status=status.HTTP_200_OK
            )

        item.quantity = quantity
        item.save()

        return Response(
            {"message": "Cart updated"},
            status=status.HTTP_200_OK
        )

    # ❌ DELETE /cart/{item_id}/
    def destroy(self, request, pk=None):
        cart = self.get_cart(request)

        try:
            item = CartItem.objects.get(id=pk, cart=cart)
            item.delete()
            return Response(
                {"message": "Item removed"},
                status=status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )