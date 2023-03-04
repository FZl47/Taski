from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


app_name = 'account'
urlpatterns = [
    path('register/',views.Register.as_view(),name='register'),
    path('login/',views.Login.as_view(),name='login'),
    path('update-user/',views.UserUpdate.as_view(),name='update_user'),
    path('reset-password/',views.ResetPassword.as_view(),name='reset_password'),
    path('reset-password-code/',views.ResetPasswordCode.as_view(),name='reset_password_code'),
    path('delete-user/',views.UserDelete.as_view(),name='delete_user'),
    path('token/refresh/',views.AccessToken.as_view(),name='access_token'),
]


