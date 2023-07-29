from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def chatbot(request):
    return render(request, 'ChatBot360/chatbot.html')
