from django.urls import path
from .views import RegisterAPIView, CustomTokenObtainPairView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token"),
]