from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import os
import uuid
from django.core.validators import RegexValidator
from django.utils.timezone import now
import face_recognition
import datetime
from enum import Enum

# Create your models here.
#User = get_user_model()


class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)

User = get_user_model()

def unique_file_path(instance, filename):
    # Save original file name in model
    instance.original_file_name = filename
    # Get new file name/upload path
    base, ext = filename.split(".")
    newname = "%s%s%s" % (uuid.uuid4(),".", ext)
    arq = open("./.name.txt", 'w')
    arq.write(newname)
    arq.close()
    return os.path.join('students', newname)

def photo_code_creater():
    arq = open ("./.name.txt", 'r')
    name = arq.read()
    image = face_recognition.load_image_file("./media/students/"+name)
    arq.close()
    arq = open("./.name.txt", 'w')
    arq.write("")
    arq.close()
    image = face_recognition.face_encodings(image)[0]
    print(image)
    return image

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE, primary_key=True)
    fullname = models.CharField(max_length=255)
    matricula = models.CharField(max_length=10)
    photo = models.ImageField(upload_to=unique_file_path, default = 'students/no-img.jpg')
    photo_code = models.TextField(max_length=2048, default = photo_code_creater)

class Group(models.Model):
	teacher = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'group')
	name = models.CharField(max_length=255)
	creditos = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
	senha_de_acesso = models.CharField(max_length=255,)

	# def __str__(self):
	# 	return self.name

class RegisteredGroup(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registered_groups')
	group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='registered_groups')

# class ClassTimeChoice(Enum):   # A subclass of Enum
#     1 = "06:00-8:00"
#     2 = "08:00-10:00"
#     3 = "10:00-12:00"
#     4 = "12:00-14:00"
#     5 = "14:00-16:00"
#     6 = "16:00-18:00"
#     7 = "18:00-20:00"
#     8 = "20:00-22:00"
#     9 = "22:00-00:00"

class AttendanceSheet(models.Model):
	registered = models.ForeignKey(RegisteredGroup, on_delete=models.CASCADE, related_name = 'attendance_sheet')
	present = models.CharField(max_length = 25,default="Chamada nao realizada")
	date = models.DateField(default=datetime.date.today)
	CLASS_TIMES = (
        ('0', '06:00 - 08:00'),
        ('1', '08:00 - 10:00'),
        ('2', '10:00 - 12:00'),
		('3', '12:00 - 14:00'),
		('4', '14:00 - 16:00'),
		('5', '16:00 - 18:00'),
		('6', '18:00 - 20:00'),
		('7', '20:00 - 22:00'),
		('8', '22:00 - 00:00'),
    )
	time = models.CharField(max_length=1, choices=CLASS_TIMES)
