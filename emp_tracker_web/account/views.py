from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
import requests
import json
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

URL = "http://softmindtracker.herokuapp.com"

@csrf_protect
def login(request):
    if request.method == "POST":
        url = f"{URL}/api/login/"
        username = request.POST.get('username')
        password = request.POST.get('password')

        login = requests.post(url, data={'username': username,
                                        'password': password})
        
        response = login.json()
        try:
            if login.status_code == 200:
                token = response['token']
                request.session['token'] = token

                request.session['username'] = request.POST['username']
                return redirect('account:home')

            else:
                messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')
        except:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
    return render(request, "account/login.html")


def home(request):
    try:
        if request.session['token']:
            username = request.session['username']
            token = request.session['token']
            params = {'username': username, 'token':token}
            # print(params)
            return render(request, "dashboard/home.html", params)
        else:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
    except:
        messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')





def register(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
            
        if request.method == "POST":
            url = f"{URL}/api/register/"
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                data = {
                    "username" : username ,
                    "email" : email ,
                    "password" : password2 ,
                }

                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                response = requests.post(url, data=data, headers=headers)
                user = response.json()
                try:
                    if user['username'] == ['A user with that username already exists.']:
                        messages.error(request,'The username already exists. Please use a different username',extra_tags = 'alert alert-warning alert-dismissible show' )
                        return redirect('account:register')
                    else:
                        messages.error(request,'New User Registered successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                        return redirect('account:register')
                except:
                    messages.error(request,'New User Registered successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                    return redirect('account:register')
            else:
                messages.error(request,'Password mismatch',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:register')        
        username = request.session['username']
        params = {'username': username}
        return render(request, "account/register.html", params)
    except:
        messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

def employee_list(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        emp_url = f"{URL}/api/employees/list/"
        address_url = f"{URL}/api/employeesaddress/list/"
        family_url = f"{URL}/api/employeesfamily/list/"
        account_url = f"{URL}/api/employeesbankaccount/list/"

        token = request.session['token']
        headers = {'Authorization' : f'Token {token}'}
        emp_list = requests.get(emp_url, headers=headers)
        address_list = requests.get(address_url, headers=headers)
        family_list = requests.get(family_url, headers=headers)
        account_list = requests.get(account_url, headers=headers)

        emp_data = emp_list.json()
        address_data = address_list.json()
        family_data = family_list.json()
        account_data = account_list.json()

        username = request.session['username']
        params = {'emps_list': emp_data, 'address_data': address_data, 'family_data': family_data, 'account_data': account_data, 'username': username, 'title':'Profile'}
        return render(request, "dashboard/employee_list.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')
    

def add_employee_view(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        if request.method == "POST":
            url = f"{URL}/api/employee/create/"
            employeeid        = request.POST.get('employeeid')
            firstname         = request.POST.get('firstname')
            lastname          = request.POST.get('lastname')
            gender            = request.POST.get('gender')
            email             = request.POST.get('email')
            phonenumber       = request.POST.get('phonenumber')
            dateofbirth       = request.POST.get('dateofbirth')
            religion          = request.POST.get('religion')
            nationality       = request.POST.get('nationality')
            is_phone_verified = request.POST.get('is_phone_verified')
            is_email_verified = request.POST.get('is_email_verified')

            data = {
                "Employee_Id": employeeid ,
                "First_Name": firstname ,
                "Last_Name": lastname ,
                "Gender": gender ,
                "Email": email ,
                "Phone": phonenumber ,
                "Date_Of_Birth": dateofbirth ,
                "Religion": religion ,
                "Nationality": nationality ,
                "Is_Phone_Verified": is_phone_verified ,
                "Is_Email_Verified": is_email_verified ,            
            }
            try:
                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                emp_create = requests.post(url, data=data, headers=headers)
                emp_data = emp_create.json()
                messages.error(request,'New Employee Details Added successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('account:create_employee')
            except:
                messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')
        username = request.session['username']
        params = {'username': username, 'title':'Add Employee Personal Info Form'}
        return render(request, "dashboard/create_employee.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

def add_employee_address_view(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        if request.method == "POST":
            url = f"{URL}/api/employeeaddress/create/"
            employeeid          = request.POST.get('employeeid')
            addressline1        = request.POST.get('addressline1')
            addressline2        = request.POST.get('addressline2')
            street              = request.POST.get('street')
            city                = request.POST.get('city')
            zipcode             = request.POST.get('zipcode')
            addresstype         = request.POST.get('addresstype')
            is_address_verified = request.POST.get('is_address_verified')

            data = {
                "Employee_Id": employeeid ,
                "Address_Line1": addressline1 ,
                "Address_Line2": addressline2 ,
                "Street": street ,
                "City": city ,
                "Zip_Code": zipcode ,
                "Address_Type": addresstype ,
                "Is_Address_Verified": is_address_verified ,
            }
            try:
                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                emp_create_address = requests.post(url, data=data, headers=headers)
                emp_data = emp_create_address.json()
                messages.error(request,'New Employee Address Details Added successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('account:create_employee_address')
            except:
                messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')
        username = request.session['username']
        params = {'username': username, 'title':'Add Employee Address Info Form'}
        return render(request, "dashboard/create_employee_address.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')


def add_employee_family_view(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
        if request.method == "POST":
            url = f"{URL}/api/employeefamily/create/"
            employeeid          = request.POST.get('employeeid')
            firstname           = request.POST.get('firstname')
            lastname            = request.POST.get('lastname')
            relationshiptype    = request.POST.get('relationshiptype')
            occupation          = request.POST.get('occupation')
            phone               = request.POST.get('phone')
            email               = request.POST.get('email')
            is_details_verified = request.POST.get('is_details_verified')
            is_phone_verified   = request.POST.get('is_phone_verified')
            is_email_verified   = request.POST.get('is_email_verified')

            data = {
                "Employee_Id": employeeid ,
                "First_Name": firstname ,
                "Last_Name": lastname ,
                "Relationship_Type": relationshiptype ,
                "Occupation": occupation ,
                "Phone": phone ,
                "Email": email ,
                "Is_Details_Verified": is_details_verified ,
                "Is_Phone_Verified": is_phone_verified ,
                "Is_Email_Verified": is_email_verified ,
            }
            try:
                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                emp_create_family = requests.post(url, data=data, headers=headers)
                emp_data = emp_create_family.json()
                messages.error(request,'New Employee Family Details Added successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('account:create_employee_family')
            except:
                messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')
        username = request.session['username']
        params = {'username': username, 'title':'Add Employee Family Info Form'}
        return render(request, "dashboard/create_employee_family.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')


def add_employee_bank_view(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        if request.method == "POST":
            url = f"{URL}/api/employeebankaccount/create/"
            employeeid    = request.POST.get('employeeid')
            bankname      = request.POST.get('bankname')
            accountnumber = request.POST.get('accountnumber')
            address       = request.POST.get('address')
            IFSCcode      = request.POST.get('IFSCcode')

            data = {
                "Employee_Id": employeeid ,
                "Bank_Name": bankname ,
                "Account_Number": accountnumber ,
                "Address": address ,
                "IFSC_Code": IFSCcode ,
            }
            try:
                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                emp_create_bank = requests.post(url, data=data, headers=headers)
                emp_data = emp_create_bank.json()
                messages.error(request,'New Employee Bank Account Details Added successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('account:create_employee_address')
            except:
                messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')
        username = request.session['username']
        params = {'username': username, 'title':'Add Employee Account Info Form'}
        return render(request, "dashboard/create_employee_bank.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')


def employee_profile(request, pk):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
        pk = pk
        params = {}
        try:
            emp_url = f"{URL}/api/employee/detail/{pk}"
            address_url = f"{URL}/api/employeeaddress/detail/{pk}"
            family_url = f"{URL}/api/employeefamily/detail/{pk}"
            account_url = f"{URL}/api/employeebankaccount/detail/{pk}"

            token = request.session['token']
            headers = {'Authorization' : f'Token {token}'}
            emp_list = requests.get(emp_url, headers=headers)
            address_list = requests.get(address_url, headers=headers)
            family_list = requests.get(family_url, headers=headers)
            account_list = requests.get(account_url, headers=headers)

            emp_data = emp_list.json()
            address_data = address_list.json()
            family_data = family_list.json()
            account_data = account_list.json()

            params['emp_data'] = emp_data
            params['address_data'] = address_data
            params['family_data'] = family_data
            params['account_data'] = account_data
            params['username'] = request.session['username']
            # print(params)
        except:
            messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
        return render(request, "dashboard/employee_profile.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')


def update_employee_detail(request, pk):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        pk = pk
        params = {}
        # emp_detail_url = f"{URL}/api/employee/detail/{pk}"
        if request.method == "POST":
            # Update Employee Personal Info        
            emp_url = f"{URL}/api/employee/update/{pk}"
            # employeeid        = request.POST.get('employeeid')
            firstname         = request.POST.get('firstname')
            lastname          = request.POST.get('lastname')
            gender            = request.POST.get('gender')
            email             = request.POST.get('email')
            phonenumber       = request.POST.get('phonenumber')
            dateofbirth       = request.POST.get('dateofbirth')
            religion          = request.POST.get('religion')
            nationality       = request.POST.get('nationality')
            is_phone_verified = request.POST.get('is_phone_verified')
            is_email_verified = request.POST.get('is_email_verified')

            emp_data = {
                "Employee_Id": f"{pk}",
                "First_Name": firstname ,
                "Last_Name": lastname ,
                "Gender": gender ,
                "Email": email ,
                "Phone": phonenumber ,
                "Date_Of_Birth": dateofbirth ,
                "Religion": religion ,
                "Nationality": nationality ,
                "Is_Phone_Verified": is_phone_verified ,
                "Is_Email_Verified": is_email_verified ,            
            }


            try:
                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                # emp_detail = requests.get(emp_detail_url, headers=headers)
                # emp_detail_info = emp_detail.json()
                # print(emp_detail_info)
                # params['emp_detail_info'] = emp_detail_info

                emp_update = requests.post(emp_url, data=emp_data, headers=headers)     
                emp_update_data = emp_update.json()
                print(emp_update_data)
                params['emp_data'] = emp_update_data

                messages.error(request,'Employee Personal Info Updated Successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('account:create_employee')
            except:
                messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')       

        params['username'] = request.session['username']
        params['title'] = 'Employee Personal Info Update Form'
        return render(request, "dashboard/create_employee.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

def update_address(request, pk):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        pk = pk
        params = {}
        if request.method == "POST":
            address_url = f"{URL}/api/employeeaddress/update/{pk}"
            employeeid          = request.POST.get('employeeid')
            addressline1        = request.POST.get('addressline1')
            addressline2        = request.POST.get('addressline2')
            street              = request.POST.get('street')
            city                = request.POST.get('city')
            zipcode             = request.POST.get('zipcode')
            addresstype         = request.POST.get('addresstype')
            is_address_verified = request.POST.get('is_address_verified')

            address_data = {
                "employeeid": employeeid,
                "Address_Line1": addressline1 ,
                "Address_Line2": addressline2 ,
                "Street": street ,
                "City": city ,
                "Zip_Code": zipcode ,
                "Address_Type": addresstype ,
                "Is_Address_Verified": is_address_verified ,
            }
            try:
                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                emp_address = requests.post(address_url, data=address_data, headers=headers)
                emp_address_data = emp_address.json()
                print(emp_address_data)
                params['address_data'] = emp_address_data

                messages.error(request,'Employee address Info Updated Successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('account:create_employee_address')
            except:
                messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')
            
        params['username'] = request.session['username']
        params['title'] = 'Employee address Info Update Form'
        return render(request, "dashboard/create_employee_address.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

def update_family(request, pk):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        pk = pk
        params = {}
        if request.method == "POST":
            family_url = f"{URL}/api/employeefamily/update/{pk}"
            employeeid          = request.POST.get('employeeid')
            firstname           = request.POST.get('firstname')
            lastname            = request.POST.get('lastname')
            relationshiptype    = request.POST.get('relationshiptype')
            occupation          = request.POST.get('occupation')
            phone               = request.POST.get('phone')
            email               = request.POST.get('email')
            is_details_verified = request.POST.get('is_details_verified')
            is_phone_verified   = request.POST.get('is_phone_verified')
            is_email_verified   = request.POST.get('is_email_verified')

            family_data = {
                "employeeid": employeeid,
                "First_Name": firstname ,
                "Last_Name": lastname ,
                "Relationship_Type": relationshiptype ,
                "Occupation": occupation ,
                "Phone": phone ,
                "Email": email ,
                "Is_Details_Verified": is_details_verified ,
                "Is_Phone_Verified": is_phone_verified ,
                "Is_Email_Verified": is_email_verified ,
            }
            try:
                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                emp_family = requests.post(family_url, data=family_data, headers=headers)
                emp_family_data = emp_family.json()
                print(emp_family_data)
                params['family_data'] = emp_family_data

                messages.error(request,'Employee Family Info Updated Successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('account:create_employee_family')
            except:
                messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')

        params['username'] = request.session['username']
        params['title'] = 'Employee Family Info Update Form'
        return render(request, "dashboard/create_employee_family.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

def update_account(request,pk):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        pk = pk
        params = {}
        if request.method == "POST":
            url = f"{URL}/api/employeebankaccount/update/{pk}"
            employeeid    = request.POST.get('employeeid')
            bankname      = request.POST.get('bankname')
            accountnumber = request.POST.get('accountnumber')
            address       = request.POST.get('address')
            IFSCcode      = request.POST.get('IFSCcode')

            account_data = {
                "employeeid": employeeid,
                "Bank_Name": bankname ,
                "Account_Number": accountnumber ,
                "Address": address ,
                "IFSC_Code": IFSCcode ,
            }
            try:
                token = request.session['token']
                headers = {'Authorization' : f'Token {token}'}
                emp_account = requests.post(url, data=account_data, headers=headers)
                emp_account_data = emp_account.json()
                print(emp_account_data)
                params['account_data'] = emp_account_data

                messages.error(request,'Employee Bank Account Info Updated Successfully!',extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('account:create_employee_bank_details')
            except:
                messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:login')

        params['username'] = request.session['username']
        params['title'] = 'Employee Account Info Update Form'
        return render(request, "dashboard/create_employee_bank.html", params)
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

def reset_password(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        if request.method == "POST":
            url = f"{URL}/api/change-password/"
            oldpassword = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            confirmnewpassword = request.POST.get('confirmnewpassword')

            if oldpassword == newpassword and confirmnewpassword:
                messages.warning(request,'Old Password and New Password cannot be same',extra_tags = 'alert alert-warning alert-dismissible show' )
                return redirect('account:reset_password')            
            
            if newpassword == confirmnewpassword:
                data = {
                    "old_password": oldpassword ,
                    "new_password": newpassword ,
                }
                try:
                    token = request.session['token']
                    headers = {'Authorization' : f'Token {token}'}
                    reset_password = requests.put(url, data=data, headers=headers)
                    reset_password_response = reset_password.json()
                    if reset_password_response['code'] == 200:
                        messages.success(request,'Password updated successfully',extra_tags = 'alert alert-success alert-dismissible show' )
                        return redirect('account:reset_password')
                except:
                    messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
                    return redirect('account:login')
            else:
                messages.error(request,'Password mismatch',extra_tags = 'alert alert-danger alert-dismissible show' )
                return redirect('account:reset_password')  

        return render(request, "account/recover_password.html")
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

def logout(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        url = f"{URL}/api/logout/"
        try:
            token = request.session['token']
            headers = {'Authorization' : f"Token {token}"}
            logout = requests.post(url, headers=headers)
            
            del request.session['token']
            messages.error(request,'You have successfully logged out!',extra_tags = 'alert alert-success alert-dismissible show' )
            return redirect('account:login')
        except:
            messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')

def logout_all(request):
    try:
        if not request.session['token']:
            messages.error(request,'Login failed: Invalid username or password.',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')

        url = f"{URL}/api/logoutall/"
        try:
            token = request.session['token']
            headers = {'Authorization' : f"Token {token}"}
            logout = requests.post(url, headers=headers)
            
            del request.session['token']
            messages.error(request,'You have successfully logged out from all devices!',extra_tags = 'alert alert-success alert-dismissible show' )
            return redirect('account:login')
        except:
            messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
            return redirect('account:login')
    except:
        messages.error(request,'You do not have permission to access!',extra_tags = 'alert alert-danger alert-dismissible show' )
        return redirect('account:login')
