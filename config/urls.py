"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from daddik.views import CreateUserView , UserDashboardView , SendMessageView , GetUserMessagesView , ChangeSubscriptionPlanView , UpdateUserView , SubscriptionHistoryView 
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('daddik.urls')),
    path('api/calculator/', include('calculator.urls')),
    path('api/search/', include('search_engine.urls')),
    path('api/user/register/', CreateUserView.as_view() , name='register'),
    path('api/token/', TokenObtainPairView.as_view() , name='get_token'),
    path('api/subscription/history/', SubscriptionHistoryView.as_view(), name='subscription-history'),
    path('api/token/refresh/', TokenRefreshView.as_view() , name='refresh'),
    path('api/user/dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('api/user/update/', UpdateUserView.as_view(), name='update_user'),
    path('api/send-messages/', SendMessageView.as_view(), name='send-message'),
    path('api/messages/', GetUserMessagesView.as_view(), name='my-messages'),
    path('api/subscription/', ChangeSubscriptionPlanView.as_view(), name='subscription'),
]
