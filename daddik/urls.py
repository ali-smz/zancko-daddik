from django.urls import path
from .views import LegalPersonViewSet , RealPersonViewSet , ProfitCalculatorViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('legal-person', LegalPersonViewSet , basename='legal-person')
router.register('real-person', RealPersonViewSet , basename= 'real-person')
router.register('calculator', ProfitCalculatorViewSet, basename='calculator')

urlpatterns = [
   
]

urlpatterns += router.urls