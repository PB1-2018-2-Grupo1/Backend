from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, TemplateView, CreateView, ListView, UpdateView
from user.forms import SignUpForm, TeacherSignUpForm, StudentSignUpForm, LoginForm
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()

class IndexPageView(TemplateView):
	template_name = 'index.html'

class SignUpView(TemplateView):
    template_name = 'signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('home.html')
        else:
            return redirect('home.html')
    return render(request, 'home.html')

"""
class UserSignupView(View):
	template_name = 'signup.html'
	form_class = SignUpForm

	def get(self, request, *args, **kwargs):
		form = SignUpForm(request.POST)
		return render(request, 'signup.html', {'form': form})

	def post(self, request, *args, **kwargs):
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
		return render(request, 'signup.html', {'form': form})
"""
class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('aluno.html')


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index.html')

class UserLoginView(FormView):
	template_name = 'login.html'
	form_class = LoginForm

	def get(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		return render(request, 'login.html', {'form': form})

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			usernamevalue = form.cleaned_data.get('username')
			passwordvalue = form.cleaned_data.get('password1')
			user = authenticate(username=usernamevalue, password=passwordvalue)
			if user is not None:
				login(request,user)
				context = {'form' : form,
				'error' : 'Sucessful login'}

				return render(request, 'index.html', context)

			else:
				context = {'form' : form,
				'error' : 'Failed to login'}

				return render(request, 'login.html', context)

		else:
			context = {'form': form}
			return render(request, 'login.html', context)
