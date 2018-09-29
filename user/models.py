from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings

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
