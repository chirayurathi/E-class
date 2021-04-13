from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth import authenticate,login as auth_login
import json

def home(request):
    return render(request,'learnerApp/home.html')
def login(request):
    if(request.user):
        redirect('dashboard')
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
def dashboard(request):
    user = CustomUser()