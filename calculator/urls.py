from .views import ProfitCalculatorViewSet ,LaborLawCalculatorViewSet , SocialSecurityculatorViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('tax', ProfitCalculatorViewSet, basename='tax-calculator')
router.register('labor', LaborLawCalculatorViewSet, basename='labor-calculator')
router.register('social', SocialSecurityculatorViewSet, basename='social-security-calculator')



urlpatterns = [
   
]

urlpatterns += router.urls