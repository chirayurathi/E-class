from django.shortcuts import render,redirect
from django.http import JsonResponse,Http404
from .models import CustomUser,Admin
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
import json

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

def adminDashboard(request):
    return render(request,'learnerApp/adminDashboard.html',context={'user':request.user})

def instituteDashboard(request):
    return render(request,'learnerApp/instituteDashboard.html')

def facultyDashboard(request):
    return render(request,'learnerApp/facultyDashboard.html')

def studentDashboard(request):
    return render(request,'learnerApp/studentDashboard.html')

def dashboard(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('login')
