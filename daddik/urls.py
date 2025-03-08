from django.urls import path
from .views import TaskViewList 
from rest_framework import routers

router = routers.DefaultRouter()

router.register('tasks', TaskViewList, basename='tasks')


urlpatterns = [
   
]

urlpatterns += router.urls