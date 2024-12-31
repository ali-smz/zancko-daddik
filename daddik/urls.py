from django.urls import path
from .views import ProfitCalculatorViewSet , UserListView
from rest_framework import routers

router = routers.DefaultRouter()

router.register('calculator', ProfitCalculatorViewSet, basename='calculator')
router.register('users', UserListView, basename='all-user')


urlpatterns = [
   
]

urlpatterns += router.urls