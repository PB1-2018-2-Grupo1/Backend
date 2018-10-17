from django.contrib import admin
from .models import User, Student, Group, RegisteredGroup

admin.site.register(Student)
admin.site.register(Group)
admin.site.register(RegisteredGroup)
