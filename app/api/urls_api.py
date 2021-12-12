from django.urls import path
from .views_api import CategoryAPIView
urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories')
]