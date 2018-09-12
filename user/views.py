from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from user.forms import SignUpForm
from django.conf import settings

def index(request):
	template_name = "index.html"
	return render(request, 'index.html')


class UserFormView(FormView):
	form_class = SignUpForm
	template_name = "signup.html"


	def register(request):
	    if request.method == 'POST':
	        f = UserCreationForm(request.POST)
	        if f.is_valid():
	            f.save()
	            messages.success(request, 'Account created successfully')
	            return redirect('index')

	    else:
	        f = UserCreationForm()

	    return render(request, 'signup.html', {'form': f})