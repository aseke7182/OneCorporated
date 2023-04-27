from django.http import HttpResponse
from rest_framework import generics, permissions, response
from rest_framework.exceptions import PermissionDenied
from .models import News, Order
from .serializers import NewsSerializer, OrderSerializer, OrderInfoSerializer
from .pagination import TenPagePagination


def ping(request):
    return HttpResponse('pong')


class NewsAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (permissions.AllowAny, )
    pagination_class = TenPagePagination


class NewsInfoAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'slug'


class OrderAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny, )
    

class OrderInfoAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderInfoSerializer
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'identification_number'

    def get_object(self):
        obj = super().get_object()
        if obj.sender is not None and self.request.user != obj.sender:
            raise PermissionDenied("You do not have permission to perform this action.")
        return obj
