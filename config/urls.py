from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 AUTH (REGISTER + JWT LOGIN + CART MERGE)
    path('api/auth/', include('accounts.urls')),

    # 📦 APPS
    path('api/products/', include('products.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/carts/', include('carts.urls')),
]