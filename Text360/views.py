from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import Room

# Create your views here.

def Text(request):
    return render(request,'Text360/base.html')

def groupVC(request):
    return render(request,'VideoChat360/error.html')


@require_POST
def create_room(request, uuid):
    name=request.POST.get('name','')
    url=request.POST.get('url', '')


    Room.objects.create(uuid=uuid, client=name,url=url)

    return JsonResponse({'message': 'room created'})
    