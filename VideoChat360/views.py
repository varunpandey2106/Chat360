from django.shortcuts import render
import random
import time
from .models import friendVCmember
from django.http import JsonResponse
import json
from agora_token_builder import RtcTokenBuilder

# Create your views here.

def VideoChat360(request):
    return render(request, 'VideoChat360/base.html')

def friendVClobby(request):
    return render(request,'VideoChat360/friendVClobby.html')

def friendVC(request):
    return render(request,'VideoChat360/friendVC.html')

def groupVC(request):
    return render(request,'VideoChat360/groupVC.html')

def getToken(request):
    appId = "YOUR APP ID"
    appCertificate = "YOUR APP CERTIFICATE"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)

