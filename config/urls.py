from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),

    # 📦 APPS
    path('api/products/', include('products.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/carts/', include('carts.urls')),
]