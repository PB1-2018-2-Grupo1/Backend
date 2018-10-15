from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, TemplateView, CreateView, ListView, UpdateView
from user.forms import SignUpForm, TeacherSignUpForm, StudentSignUpForm, LoginForm, GroupForm, StudentRegisterGroupForm
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Group, User
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
        return redirect('/students')


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
        return redirect('/teachers')

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

class GroupCreateView(CreateView):
	model = Group
	fields = ('name', 'creditos', 'senha_de_acesso')
	template_name = 'group_add_form'

	def get(self, request, *args, **kwargs):
		form = GroupForm(request.POST)
		return render(request, 'group_add_form.html', {'form': form})

	def form_valid(self, form):
		group = form.save(commit=False)
		group.teacher = self.request.user
		group.save()
		messages.success(self.request, 'A turma foi criada com sucesso')
		return redirect('')

class StudentGroupListView(ListView):
	model = Group
	context_object_name = 'groups'
	template_name = 'group_list.html'

	def get_queryset(self):
		student = self.request.user.student
		queryset = Group.objects.all()
		return queryset
"""
class StudentRegisterGroupView(FormView):
	model = Group
	template_name = 'group_register.html'

	def get(self, request):
		form = StudentRegisterGroupForm(request.POST)
		return render (request, 'group_register.html', {'form':form})

	def post(self, request):
		student = self.request.user.student
		form = StudentRegisterGroupForm(request.POST)

		if form.is_valid():
			code_value = form.cleaned_data.get('senha_de_acesso')
		return render(request, 'group_list.html')
"""

def enter_group(request,pk):
	group = get_object_or_404(Group, pk = pk)
	student = request.user.student

	if request.method == 'POST':
		form = StudentRegisterGroupForm()
		if form.is_valid():
			with transaction.atomic():
				student_pass = form.save(commit=False)
				student_pass.student = student
				student_pass.save()
