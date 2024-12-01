from django.urls import path, include
from rest_framework.authtoken import views
from .views import *

urlpatterns = [
    path('api/users/', UserCreateView.as_view(), name='create_user'),
    path('api/token/', CustomAuthToken.as_view(), name='token_obtain'),
    path('api/protected/', ProtectedView.as_view(), name='protected_view'),
    path('api/change-password/', change_password, name='change_password_url')
]