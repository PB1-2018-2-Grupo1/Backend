from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, TemplateView
from user.forms import SignUpForm
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from user.forms import SignUpForm, LoginForm

class IndexPageView(TemplateView):
	template_name = 'index.html'

class GuestOnlyView(View):
	def dispatch(self, request, *args, **kwargs):
		return HttpResponse('/teste/')

		return redirect('prapqp')

class UserSignupView(View):
	template_name = 'signup.html'
	form_class = SignUpForm

	def get(self, request, *args, **kwargs):
		return render(request, 'signup.html')

	def post(self, request, *args, **kwargs):
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
		return render(request, 'signup.html', {'form': form})

class UserLoginView(FormView):
	template_name = 'login.html'
	form_class = LoginForm

	def get(self, request, *args, **kwargs):
		return render(request, 'login.html')

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			matriculavalue = form.cleaned_data.get('matricula')
			passwordvalue = form.cleaned_data.get('password1')
			user = authenticate(username=uservalue, password=passwordvalue)
			if user is not None:
				login(request,user)
				context = {'form' : form,
				'error' : 'Sucessful login'}

				return render(request, 'index.html')

			else:
				context = {'form' : form,
				'error' : 'Failed to login'}

				return render(request, 'login.html', {'form' : form})

		else:
			context = {'form': form}
			return render(request, 'login.html')
