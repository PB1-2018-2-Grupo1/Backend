from django.contrib import admin
from .models import User, Student, Group, RegisteredGroup, AttendanceSheet

admin.site.register(Student)
admin.site.register(Group)
admin.site.register(RegisteredGroup)
admin.site.register(AttendanceSheet)
