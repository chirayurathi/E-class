from django.shortcuts import render,redirect
from django.http import JsonResponse,Http404
from .models import *
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
import json
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .forms import *
from copy import deepcopy

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request,'learnerApp/home.html')

def login(request):
    if request.user.is_authenticated :
        return redirect('dashboard')
    else:
        if(request.method == 'POST'):
            user_data = json.loads(request.body)
            print(user_data)
            user = authenticate(username=user_data['username'],password=user_data['password'])
            if user is None:
                return JsonResponse({'message':"Invalid Email or Password"},status="500")
            else:
                auth_login(request,user)
                return JsonResponse({'message':"success"})
        else:
            return render(request,'learnerApp/login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def allUser(request):
    print(Institute.objects.all())
    return render(request,'learnerApp/adminDashboard.html')

def adminDashboard(request):
    instituteList = Institute.objects.all()
    return render(request,'learnerApp/adminDashboard.html',context={'user':request.user,'instituteList':instituteList})

def instituteDashboard(request):
    return render(request,'learnerApp/instituteDashboard.html',context={'user':request.user})

def facultyDashboard(request):
    return render(request,'learnerApp/facultyDashboard.html',context={'user':request.user})

def studentDashboard(request):
    return render(request,'learnerApp/studentDashboard.html',context={'user':request.user})

@login_required(login_url="/login/")
def dashboard(request):
    if request.user.is_admin:
        return adminDashboard(request)
    elif request.user.is_institute:
        return instituteDashboard(request)
    elif request.user.is_faculty:
        return facultyDashboard(request)
    elif request.user.is_student:
        return studentDashboard(request)
    else:
        raise Http404("User role does not exist")

@login_required(login_url="/login/")
def profile(request):
    if request.method == 'POST':
        form = None
        if request.user.is_admin:
            form = AdminForm(request.POST,instance=Admin(user=request.user))
            admin = Admin.objects.get(user=request.user)
            admin.first_name = form.cleaned_data['first_name']
            admin.last_name = form.cleaned_data['last_name']
            admin.admin_number = form.cleaned_data['admin_number']
            admin.save()
            print(model_to_dict(admin))
        elif request.user.is_institute:
            form = InstituteForm(request.POST,instance=Institute(user=request.user))
        elif request.user.is_faculty:
            form = FacultyForm(request.POST,instance=Faculty(user=request.user))
        elif request.user.is_student:
            form = StudentForm(request.POST,instance=Student(user=request.user))
        else:
            raise Http404("User role does not exist")   
        # form.save()
        return redirect('dashboard')  
    else:
        form = None
        if request.user.is_admin:
            form = AdminForm(instance=Admin(user=request.user))
        elif request.user.is_institute:
            form = InstituteForm(instance=Institute(user=request.user))
        elif request.user.is_faculty:
            form = FacultyForm(instance=Faculty(user=request.user))
        elif request.user.is_student:
            form = StudentForm(instance=Student(user=request.user))
        else:
            raise Http404("User role does not exist")
        # print(form)
        return render(request,'learnerApp/profile.html',context={'user':request.user,'profile':profile,'form':form})
    


def addInstitute(request):
    if request.method == "POST":
        user  = CustomUser.objects.create_user(user_email=request.POST.get('user_email'),role="institute",password=request.POST.get('password'))
        user.save()
        Institute.objects.create(user=user,institute_name=request.POST.get('institute_name'),institute_address=request.POST.get('institute_address'),institute_id=request.POST.get('institute_id')).save()
        return redirect('dashboard')
    else:
        extraFields = [
            {
                'label':"Institute Name",
                'name':'institute_name',
                'type':'text'
            },
            {
                'label':"Institute Id",
                'name':'institute_id',
                'type':'number'
            },
            {
                'label':"Institute Address",
                'name':'institute_address',
                'type':'text'
            },
            {
                'label':"Institute Number",
                'name':'institute_number',
                'type':'number'
            }
        ]
        return render(request,'learnerApp/addUser.html',context={'extraFields':extraFields})

def addFaculty(request):
    if request.method == "POST":
        user  = CustomUser.objects.create_user(user_email=request.POST.get('user_email'),role="faculty",password=request.POST.get('password'))
        user.save()
        Faculty.objects.create(user=user,faculty_id=request.POST.get('faculty_id'),faculty_number=request.POST.get('faculty_number'),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'),institute=Institute(user=request.user)).save()
        return redirect('dashboard')
    else:
        extraFields = [
            {
                'label':"First Name",
                'name':'first_name',
                'type':'text'
            },
            {
                'label':"Last Name",
                'name':'last_name',
                'type':'text'
            },
            {
                'label':"Faculty Id",
                'name':'faculty_id',
                'type':'number'
            },
            {
                'label':"Faculty Number",
                'name':'faculty_number',
                'type':'number'
            }
        ]
        return render(request,'learnerApp/addUser.html',context={'extraFields':extraFields})