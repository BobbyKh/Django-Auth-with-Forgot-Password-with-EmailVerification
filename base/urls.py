from django.urls import include, path

from base import views


urlpatterns = [
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", views.login, name="login"),
    path ("logout/", views.logoutView, name="logout"),
    path('accounts/forgotpassword/', views.forgotpassword, name="forgotpassword"),
    path("verify_token/", views.verify_token, name="verify_token"),
    path('user_details/<int:id>/edit/', views.user_details_edit, name='user_details_edit'),
]
