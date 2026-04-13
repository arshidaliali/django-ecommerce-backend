from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import RegisterSerializer
from carts.models import Cart, CartItem

User = get_user_model()
# =========================
# REGISTER API
# =========================
class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# =========================
# CUSTOM JWT LOGIN + CART MERGE
# =========================
class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        # 🔹 Ensure session exists for guest cart
        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key
        

        # 🔹 Standard JWT response
        response = super().post(request, *args, **kwargs)

        # 🔥 If login successful → merge carts
        if response.status_code == 200:
            username = request.data.get("username")

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return response

            self.merge_cart(user, session_id)

        return response

    def merge_cart(self, user, session_id):

        guest_cart = Cart.objects.filter(session_id=session_id).first()
        if not guest_cart:
            return

        user_cart, _ = Cart.objects.get_or_create(user=user)

        for item in guest_cart.items.all():
            user_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=item.product,
                defaults={
                    "quantity": item.quantity,
                    "price": item.price
                }
            )

            if not created:
                user_item.quantity += item.quantity
                user_item.save()

        guest_cart.delete()