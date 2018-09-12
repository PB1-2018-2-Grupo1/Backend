from django.urls import path
from . import views

urlpatterns = [
	path('signup', views.UserFormView.as_view(success_url="index"), name = 'signup'),
	path('index', views.index , name = 'index'),
	]