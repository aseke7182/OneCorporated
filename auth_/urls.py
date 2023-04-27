from django.urls import path
from .views import ping, UserRegistrationAPIView, UserLoginAPIView, UserProfileAPIView

urlpatterns = [
    path('ping', ping),
    path('register', UserRegistrationAPIView.as_view()),
    path('login', UserLoginAPIView.as_view()),
    path('profile', UserProfileAPIView.as_view()),
]
