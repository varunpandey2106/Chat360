from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate

# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def register(request):
    if request.method=='POST':
        form= UserRegistrationForm(request.POST) #instantiate user creation form with POST data

        if form.is_valid():
            form.save()
        username=form.cleaned_data.get("username") #validated form data is in form.cleaned_data dictionary
        messages.success(request, f'Your account has now been created and you can login!') #flash message
        return redirect('login')
    
    else:
        form=UserRegistrationForm()
    
    form=UserRegistrationForm()
    return render(request,'home/register.html',{'form':form})

def user_login(request):
    err = None
    if request.user.is_authenticated:
        return redirect("user_login")
    
    if request.method == 'POST':
        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("features")
        
        else:
            err = "Invalid Credentials"
        
        
    context = {"error": err}
    return render(request, "home/login.html", context)

def features(request):
    return render(request,'home/features.html')





