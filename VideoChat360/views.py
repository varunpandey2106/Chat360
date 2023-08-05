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
    return render(request,'VideoChat360/friendVClobby.html')


def groupVC(request):
    return render(request,'VideoChat360/groupVC.html')
                  
                  

def getToken(request):
    appId = "0b7e3d19eefe4172b5ac32282c34b44d"  # Replace with your actual Agora App ID
    appCertificate = "b9f3ebf7a27849d58e3c5c5b0cdf43ed"  # Replace with your actual App Certificate
    channelName = request.GET.get('friendVC')  # Get the channel name from the request parameter
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds

    token_url = f"https://api.agora.io/v1/token?appid={appId}&uid={uid}&channelName={channelName}&expiredTs={privilegeExpiredTs}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{appId}:{appCertificate}'.encode()).decode()}"
    }

    response = requests.post(token_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        token = data.get('token', '')
        return JsonResponse({'token': token, 'uid': uid})
    else:
        return JsonResponse({'error': 'Failed to generate token'}, status=response.status_code)


   

def friendVC(request):
    return render(request,'VideoChat360/friendVC.html')

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