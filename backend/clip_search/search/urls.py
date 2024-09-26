# search/urls.py
from django.urls import path
from .views import ImageSearchView

urlpatterns = [
    path('search/', ImageSearchView.as_view(), name='image_search'),
]
