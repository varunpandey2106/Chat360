from django.shortcuts import render, redirect

# Create your views here.

def Text(request):
    return render(request,'Text360/Text.html')

def groupVC(request):
    return render(request,'VideoChat360/error.html')