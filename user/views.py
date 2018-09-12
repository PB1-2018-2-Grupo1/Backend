from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, TemplateView
from user.forms import SignUpForm
from django.conf import settings
from django.urls import reverse_lazy

class IndexPageView(TemplateView):
	template_name = 'index.html'
	
class GuestOnlyView(View):
	def dispatch(self, request, *args, **kwargs):
		return HttpResponse('/teste/')

		return redirect('prapqp')

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			"""
			username = form.cleaned_data['username'],
			matricula = form.cleaned_data['matricula'],
			fullname = form.cleaned_data['fullname'],
			email = form.cleaned_data['email'],
			password = form.cleaned_data['password1']
			"""
			messages.success(request, 'Account created successfully')

			return redirect('signup')

	else:
		f = SignUpForm()
		return render(request, 'signup.html', {'form': f})