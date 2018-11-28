from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView, TemplateView, CreateView, ListView, UpdateView, DetailView, DeleteView
from user.forms import SignUpForm, TeacherSignUpForm, StudentSignUpForm, LoginForm, GroupForm, StudentRegisterGroupForm, TeacherAttendanceSheetCreateForm
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Group, User, RegisteredGroup, AttendanceSheet, Student
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class IndexPageView(TemplateView):
	template_name = 'index.html'

class SignUpView(TemplateView):
    template_name = 'signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('/teachers/group/registered')
        else:
            return redirect('/students/')
    return render(request, 'signup.html')

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
        return redirect('/teachers/group/add')

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
		return redirect('/home')

class StudentGroupListView(ListView):
	model = Group
	context_object_name = 'groups'
	template_name = 'group_list.html'

	def get_queryset(self):
		student = self.request.user.student
		queryset = Group.objects.exclude(registered_groups__student = student)
		return queryset

class StudentRegisterGroupView(FormView):
	model = Group
	fields = ('senha_de_acesso')
	template_name = 'group_register.html'

	def get(self, request, pk):
		group = get_object_or_404(Group, pk = pk)
		form = StudentRegisterGroupForm(request.POST, request.FILES)
		return render (request, 'group_register.html', {'form':form})

	def post(self, request, pk):
		group = get_object_or_404(Group, pk = pk)
		student = self.request.user.student
		group_pass = group.senha_de_acesso
		form = StudentRegisterGroupForm(request.POST)
		if form.is_valid():
			code_value = form.cleaned_data.get('senha_de_acesso')
			if code_value == group_pass:
				# student = Student.objects.get(pk=course_id)
				registered_group = RegisteredGroup.objects.create(group=group, student=student)
				return render(request, 'teste.html')
		return render(request, 'group_list.html')

class StudentGroupDetailedView(DetailView):
	model = RegisteredGroup
	context_object_name = 'registered_group'
	template_name = 'student_group_detailed.html'


class StudentRegisteredGroupsListView(ListView):
	model = RegisteredGroup
	context_object_name = 'registered_groups'
	template_name = 'group_registered.html'

	def get_queryset(self):
		student = self.request.user.student
		queryset = RegisteredGroup.objects.filter(student = student, deleted_at = None)

		return queryset

class StudentRegisteredGroupDeleteView(DeleteView):
	model = RegisteredGroup
	template_name = 'student_group_delete.html'
	success_url = reverse_lazy('students:group_registered')

	def delete(self, request, pk, *args, **kwargs):
		registered_group = get_object_or_404(RegisteredGroup, pk = pk)
		messages.success(request, 'The student %s was deleted with success!' % registered_group.student.fullname)
		return super().delete(request, *args, **kwargs)


class TeacherGroupListView(ListView):
	model = Group
	context_object_name = 'groups'
	template_name = 'teacher_group_registered.html'

	def get_queryset(self):
		teacher = self.request.user
		queryset = Group.objects.filter(teacher = teacher)

		return queryset

class TeacherDetailedGroupView(DetailView):
	model = Group
	context_object_name = 'group'
	template_name = 'teacher_group_detailed.html'

	def get_context_data(self, **kwargs):
		group = self.get_object()
		registered_groups = group.registered_groups.select_related('student__user')
		attendance_sheets  = AttendanceSheet.objects.all()
		extra_context = {
            'registered_groups': registered_groups,
			'attendance_sheets': attendance_sheets,
        }
		kwargs.update(extra_context)

		return super().get_context_data(**kwargs)

	def get_queryset(self):
		return self.request.user.group.all()

class TeacherRemoveStudentDeleteView(DeleteView):
	model = RegisteredGroup
	template_name = 'student_group_delete.html'

	def delete(self, request, pk, *args, **kwargs):
		registered_group = get_object_or_404(RegisteredGroup, pk = pk)
		registered_group.is_deleted = True
		registered_group.deleted_at = timezone.localtime(timezone.now())
		registered_group.deleted_by = self.request.user
		messages.success(request, 'The student %s was deleted with success!' % registered_group.student.fullname)
		registered_group.save()
		return redirect('/home')

def create_sheet(request, pk):
		group_obj = get_object_or_404(Group, pk=pk, teacher=request.user)

		if request.method == 'POST':
			form = TeacherAttendanceSheetCreateForm(request.POST)

			if form.is_valid():
				registered_group = RegisteredGroup.objects.filter(group = group_obj, deleted_at = None)
				attendance = form.save(commit=False)
				for object in registered_group:
					attendance.registered = object
					AttendanceSheet.objects.create(registered = object, date = attendance.date)
				messages.success(request, 'A chamada foi criada')
				return redirect('/home')
		else:
			form = TeacherAttendanceSheetCreateForm()

		return render(request, 'attendance_register.html', {'group_obj': group_obj, 'form': form})
