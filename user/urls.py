from django.urls import path
from . import views

urlpatterns = [
	path('signup', views.signup , name = 'signup'),
	path('index', views.IndexPageView.as_view() , name = 'index'),
	]