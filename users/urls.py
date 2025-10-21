from django.urls import path
from .views import UserRegisterView, UserConfirmView, UserLoginView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('confirm/', UserConfirmView.as_view(), name='user-confirm'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]
