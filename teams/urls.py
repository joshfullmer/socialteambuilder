from django.urls import path

from . import views

app_name = 'teams'
urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
]
