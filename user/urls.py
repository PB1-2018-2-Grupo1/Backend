from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),

    path('students/', include(([
        path('', StudentGroupListView.as_view(), name = 'group_list'),
        path('group/register/<int:pk>', StudentRegisterGroupView.as_view(), name = 'group_register'),
        path('group/registered/', StudentRegisteredGroupsListView.as_view(), name = 'group_registered'),
        path('group/registered/<int:pk>', StudentGroupDetailedView.as_view(), name = 'group_detailed'),
        path('group/registered/<int:pk>/delete', StudentRegisteredGroupDeleteView.as_view(), name = 'group_delete'),
    ], 'user'), namespace = 'students')),

    path('teachers/', include(([
        path('', home, name = 'group_change_list'),
        path('group/add/', GroupCreateView.as_view(), name = 'group_add'),
        path('group/registered', TeacherGroupListView.as_view(), name = 'group_register'),
        path('group/registered/<int:pk>', TeacherDetailedGroupView.as_view(), name = 'group_detailed'),
        path('group/registered/<int:pk>/attendance', create_sheet, name = 'attendance_create'),
        path('group/registered/<int:pk>/delete', TeacherRemoveStudentDeleteView.as_view(), name = 'group_delete'),


    ], 'user'), namespace = 'teachers'))
]
