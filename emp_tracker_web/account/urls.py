from django.contrib import admin
from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('logout/all/', views.logout_all, name='logout_all'),
    path('passwordreset/', views.reset_password, name='reset_password'),

    path('register/', views.register, name='register'),
    path('employee/list/', views.employee_list, name='employee_list'),
    path('create/employee/', views.add_employee_view, name='create_employee'),
    path('create/employee/address/', views.add_employee_address_view, name='create_employee_address'),
    path('create/employee/family/', views.add_employee_family_view, name='create_employee_family'),
    path('create/employee/bankdetails/', views.add_employee_bank_view, name='create_employee_bank_details'),
    path('employee/profile/<str:pk>/', views.employee_profile, name='employee_profile'),
    # path('employee/edit/profile/<str:pk>/', views.employee_edit_profile, name='employee_edit_profile'),

    # Employee Updation Form URL
    path('employee/update/personalinfo/<str:pk>/', views.update_employee_detail, name='update_employee_detail'),
    path('employee/update/addressinfo/<str:pk>/', views.update_address, name='update_address'),
    path('employee/update/familyinfo/<str:pk>/', views.update_family, name='update_family'),
    path('employee/update/accountinfo/<str:pk>/', views.update_account, name='update_account'),
]