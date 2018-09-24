from django.urls import path
from . import views

urlpatterns = [
	path('signup', views.UserSignupView.as_view() , name = 'signup'),
	path('login', views.UserLoginView.as_view(), name = 'login'),
	path('', views.IndexPageView.as_view() , name = 'index'),
	]
