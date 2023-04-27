from django.urls import path
from .views import ping, NewsAPIView, NewsInfoAPIView, OrderAPIView, OrderInfoAPIView

urlpatterns = [
    path('ping', ping),
    path('news', NewsAPIView.as_view()),
    path('news/<str:slug>', NewsInfoAPIView.as_view()),
    path('order', OrderAPIView.as_view()),
    path('order/<str:identification_number>', OrderInfoAPIView.as_view()),
]
