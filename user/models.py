from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import RegexValidator

# Create your models here.
#User = get_user_model()


class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)

User = get_user_model()

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE, primary_key=True)
    fullname = models.CharField(max_length=255)
    matricula = models.CharField(max_length=10)

class Group(models.Model):
	teacher = models.ForeignKey(User, on_delete=models.CASCADE)
	student = models.ManyToManyField(Student)
	name = models.CharField(max_length=255)
	creditos = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
	senha_de_acesso = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class RegisteredGroup(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registered_groups')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='registered_groups')
