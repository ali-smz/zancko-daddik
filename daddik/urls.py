from django.urls import path
from .views import ProfitCalculatorViewSet , UserListView , TaskViewList ,LaborLawCalculatorViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('tax-calculator', ProfitCalculatorViewSet, basename='tax-calculator')
router.register('labor-calculator', LaborLawCalculatorViewSet, basename='labor-calculator')
router.register('users', UserListView, basename='all-user')
router.register('tasks', TaskViewList, basename='tasks')


urlpatterns = [
   
]

urlpatterns += router.urls