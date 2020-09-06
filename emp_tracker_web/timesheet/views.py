from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib import messages
import datetime
import requests
import json
from django.http import HttpResponseRedirect

URL = "http://softmindtracker.herokuapp.com"

def employee_timesheet(request):
    params = {}

    emp_url = f"{URL}/api/employees/list/"
    token = request.session['token']
    headers = {'Authorization' : f'Token {token}'}
    emp_list = requests.get(emp_url, headers=headers)
    emp_data = emp_list.json()
    # print(emp_data)
    params['emp_data'] = emp_data

    # project_url = f"{URL}/timesheet/project/list/"
    # token = request.session['token']
    # headers = {'Authorization' : f'Token {token}'}
    # project_list = requests.get(project_url, headers=headers)
    # project_data = project_list.json()
    # # print(project_data)
    # params['project_data'] = project_data

    # activity_url = f"{URL}/timesheet/workactivity/list/"
    # token = request.session['token']
    # headers = {'Authorization' : f'Token {token}'}
    # activity_list = requests.get(activity_url, headers=headers)
    # activity_data = activity_list.json()
    # # print(activity_data)
    # params['activity_data'] = activity_data

    # location_url = f"{URL}/timesheet/worklocation/list/"
    # token = request.session['token']
    # headers = {'Authorization' : f'Token {token}'}
    # location_list = requests.get(location_url, headers=headers)
    # location_data = location_list.json()
    # # print(location_data)
    # params['location_data'] = location_data

    
    if request.method == "POST":
        timesheet_url = f"{URL}/timesheet/employeetimesheet/list/"
        employeeid = request.POST.get('employeeid')
        project    = request.POST.get('project')
        activity   = request.POST.get('activity')
        location   = request.POST.get('location')
        status     = request.POST.get('status')
        starttime  = request.POST.get('starttime')
        endtime    = request.POST.get('endtime')

        timesheet_data = {
            "Employee_Id": employeeid ,
            "Project": project ,
            "Activity": activity ,
            "Location": location ,
            "Status": status ,
            "Start_Time": starttime ,
            "End_Time": endtime ,
        }
        print(timesheet_data)
        
        token = request.session['token']
        headers = {'Authorization' : f'Token {token}'}
        timesheet_create = requests.post(timesheet_url, data=timesheet_data, headers=headers)
        timesheet_data = timesheet_create.json()
        print(timesheet_data)
        params['timesheet_data'] = timesheet_data
        try:            
            messages.success(request,'Employee Timesheet Added successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
            return redirect('timesheet:employee_timesheet')
        except:
            messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

    return render(request, "timesheet/create_employee_timesheet.html", params)


def view_timesheet(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
        params = {}
        try:
            timesheet_url = f"{URL}/timesheet/employeetimesheet/list/"
            token = request.session['token']
            headers = {'Authorization' : f'Token {token}'}
            timesheet_list = requests.get(timesheet_url, headers=headers)
            timesheet_data = timesheet_list.json()
            # print(len(timesheet_data))


            # timesheet_dict = timesheet_data[0]
            # timesheet_dict1 = timesheet_data[1]
            # timesheet_dict2 = timesheet_data[2]
            # print(timesheet_dict)
            # print(timesheet_dict1)
            # print(timesheet_dict2)

            # timesheet = {}
            # for emp in timesheet_data:
            #     if emp.Employee_Id not in timesheet.keys():
            #         timesheet[emp.Employee_Id] = [Employee_Id]
            #     else:
            #         timesheet[emp.Employee_Id].append(Employee_Id)
            # print(timesheet)

            # dic = {}
            # for key in timesheet_data:
            #     print(key)
            # print(dic)
            # ID = timesheet_data['Employee_Id']
            # print(ID)
            
            params['timesheet_data'] = timesheet_data
            params['username'] = request.session['username']
        except:
            messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        return render(request, "timesheet/view_employee_timesheet.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

                
def detail_timesheet(request, id):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
        id = id
        params = {}
        try:
            url = f"{URL}/timesheet/employeetimesheet/detail/{id}/"

            token = request.session['token']
            headers = {'Authorization' : f'Token {token}'}
            detail = requests.get(url, headers=headers)

            timesheet_data = detail.json()
            # print(timesheet_data)
            emp_id = timesheet_data['Employee_Id']

            emp_url = f"{URL}/api/employee/detail/{emp_id}"
            emp_list = requests.get(emp_url, headers=headers)
            emp_data = emp_list.json()
            params['emp_data'] = emp_data
            
            start_time = timesheet_data['Start_Time']
            end_time = timesheet_data['End_Time']

            start_time_str = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S+05:30")
            end_time_str = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S+05:30")

            total_work_hour = (end_time_str-start_time_str)
            # print(total_work_hour)

            params['start_time'] = start_time_str
            params['end_time'] = end_time_str
            params['total_work_hour'] = total_work_hour           

            params['timesheet_data'] = timesheet_data
            params['username'] = request.session['username']
        except:
            messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
        return render(request, "timesheet/timesheet_detail_view.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')


def testdate(request):
    dt = datetime.datetime.now
    return render(request, "timesheet/test.html", {"dt":dt})