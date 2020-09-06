from django.urls import path
from . import views

app_name = 'timesheet'
urlpatterns = [
    path('', views.employee_timesheet, name='employee_timesheet'),
    path('view/', views.view_timesheet, name='view_timesheet'),
    path('detail/<str:id>/', views.detail_timesheet, name='detail_timesheet'),
    path('testdate/', views.testdate, name='testdate'),    
]