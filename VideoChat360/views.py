from django.shortcuts import render
import random
import time
from .models import friendVCmember
from django.http import JsonResponse
import json
from agora_token_builder import RtcTokenBuilder
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
import base64


# Create your views here.

def VideoChat360(request):
    return render(request, 'VideoChat360/base.html')

def friendVClobby(request):
    return render(request,'VideoChat360/error.html')


def groupVC(request):
    return render(request,'VideoChat360/error.html')
                  
                  

def getToken(request):
    appId = "0b7e3d19eefe4172b5ac32282c34b44d"
    appCertificate = "b9f3ebf7a27849d58e3c5c5b0cdf43ed"
    channelName = request.GET.get('get_token/friendVC')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


def friendVC(request):
    return render(request, 'VideoChat360/error.html')

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = friendVCmember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        friendVC_name=data['friendVC_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    friendVC_name = request.GET.get('friendVC_name')

    member = friendVCmember.objects.get(
        uid=uid,
        friendVC_name=friendVC_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)