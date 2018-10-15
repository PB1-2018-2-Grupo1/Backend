from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),

    path('students/', include(([
        path('', StudentGroupListView.as_view(), name = 'group_list'),
        path('group/register/<int:pk>', enter_group, name = 'group_register'),

    ], 'user'), namespace = 'students')),

    path('teachers/', include(([
        path('', home, name = 'group_change_list'),
        path('group/add/', GroupCreateView.as_view(), name = 'group_add')

    ], 'user'), namespace = 'teachers'))
]
