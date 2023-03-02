from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

app_name = 'account'
urlpatterns = [
    path('register',views.Register.as_view(),name='register'),
    path('login',views.Login.as_view(),name='login'),
    path('token/refresh',views.AccessToken.as_view(),name='access_token'),
]
