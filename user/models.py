from django.db import models

# Create your models here.

class User(models.Model):

	username = models.CharField(max_length=255, null=False)
	fullname = models.CharField(max_length=255, null=False)
	is_staff = models.BooleanField('Professor', default=False)
	is_active = models.BooleanField('Ativo', default=True)
	date_joined = models.DateTimeField('Data de entrada', auto_now_add=True)