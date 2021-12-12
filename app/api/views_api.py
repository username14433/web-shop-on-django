from rest_framework.generics import ListAPIView
from .serializers import CategorySerializer
from ..models import Category


class CategoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer