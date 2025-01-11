from django.urls import path
from .views import  UserListView , TaskViewList 
from rest_framework import routers

router = routers.DefaultRouter()

router.register('users', UserListView, basename='all-user')
router.register('tasks', TaskViewList, basename='tasks')


urlpatterns = [
   
]

urlpatterns += router.urls