from django.urls import path
from .views import ProfitCalculatorViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('calculator', ProfitCalculatorViewSet, basename='calculator')

urlpatterns = [
   
]

urlpatterns += router.urls