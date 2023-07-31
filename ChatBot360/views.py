from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import openai
import json
from .models import QuestionAnswer
import datetime
from datetime import timedelta, date

# Create your views here.

open_api_key= "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"
openai.api_key= open_api_key


def chatbot(request):
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    seven_days_ago = date.today() - timedelta(days=7)
    
    questions = QuestionAnswer.objects.filter(user=request.user)
    t_questions = questions.filter(created=today)
    y_questions = questions.filter(created=yesterday)
    s_questions = questions.filter(created__gte=seven_days_ago, created__lte=today)
    
    context = {"t_questions":t_questions, "y_questions": y_questions, "s_questions": s_questions}

    return render(request, "ChatBot360/index.html", context)



def ask_openai(message):
    response=openai.ChatCompletion.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}]
    
)
    
    answer= response['choices'][0]['message']['content']
    return answer


def getValue(request):
        data=json.loads(request.body)
        message= data["msg"]
        response=ask_openai(message)
        QuestionAnswer.objects.create(user=request.user, question=message,answer=response)
        return JsonResponse({"msg":message, "res":response})
   


