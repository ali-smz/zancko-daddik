from django.urls import path
from .views import elasticsearch_insert_read , get_single_data

urlpatterns = [
    path('', elasticsearch_insert_read, name='elasticsearch_insert_read'),
    path('law/', get_single_data, name='single_law'),
]