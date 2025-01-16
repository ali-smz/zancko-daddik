from django.urls import path
from .views import DocumentCreateAPIView, DocumentSearchAPIView

urlpatterns = [
    path('documents/', DocumentCreateAPIView.as_view(), name='create-document'),
    path('', DocumentSearchAPIView.as_view(), name='search-documents'),
]
