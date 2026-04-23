from django.urls import path
from . import views

app_name = 'grievance'

urlpatterns = [
    path('',                        views.dashboard,            name='dashboard'),
    path('list/',                   views.grievance_list,       name='list'),
    path('raise/',                  views.grievance_create,     name='create'),
    path('<int:pk>/',               views.grievance_detail,     name='detail'),
    path('<int:pk>/edit/',          views.grievance_edit,       name='edit'),
    path('<int:pk>/delete/',        views.grievance_delete,     name='delete'),
    path('<int:pk>/duplicate/',     views.grievance_duplicate,  name='duplicate'),
    path('report/',                 views.report,               name='report'),
]
