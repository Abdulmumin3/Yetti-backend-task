from django.urls import path
from . import views

urlpatterns = [
	path('', views.home_page, name="home"),
	path('login/', views.login_page, name="login"),
	path('logout/', views.logout_page, name="logout"),
	path('register/', views.register_page, name="register"),
	path('csrf-attack/', views.csrf_attack, name="csrf_attack"),
]