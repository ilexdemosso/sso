from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import InputForm
import requests, base64
import json
import jwt
import os

def login(request): 
    context ={} 
    context['form']= InputForm()
    return render(request, "home.html", context)

def authorize(request):
    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            login = form.data['login']
            password = form.data['password']
            b64credentials = base64.b64encode(f'{login}:{password}'.encode())
            response1 = requests.post('http://consplusweb-dev:8097/backend/oauth/code/user?client_id=test', headers={'Authorization': f'Basic {b64credentials}'}).json()
            print("*************************************************************")
            #print(response1)
            print("*************************************************************")
            if 'code' in response1:
                code = response1['code']
                #code = 'jI2J/7ZtlAEuUs2Bm0yD8WG9g4U='

                b64secret = base64.b64encode(f'test:secret'.encode())
                response2 = requests.post(f'http://consplusweb-dev:8097/backend/oauth/code/client?code={code}', headers={'Authorization': f'Basic {b64secret}'}).json()
                if 'access_token' in response2:
                    access_token = response2['access_token']
                
                    test = {"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3V1aWQiOiI3OWYxNWM3Ny03NTQzLTJkZGMtYjg0Mi00Y2Y0YWE3MWNlMDAiLCJ1c2VyX25hbWUiOiJkZW1vQHRlc3QuY29tIiwibGFzdF9uYW1lIjoiRGVtbyIsImV4cCI6MTU5NDIxNjc4OSwibWlkZGxlX25hbWUiOiJEZW1vIiwiZmlyc3RfbmFtZSI6IkRlbW8iLCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwianRpIjoiMVNjdFZWZVRRRHVFaWxjRTJsTlBFcXVKdGRzPSIsImNsaWVudF9pZCI6InRlc3QifQ.bz5zQGl-gtH9S-9CZ1HdCDEZhG9NzmVrEqGK_ZaTb5kPK77ppYUQYRVZtxR8l3jBSNXN6z84DWHVUHQ33tU4dPx5fVHi8YDnj4YJvssISbsAKPAwt9HhVJZ8bIRFEKZipmF_6jC0cJ18vegdcKPltiyiBVWR8m01Qc-q7kFbwQkBbIiPRRnVHugVZwEn6s_6RiIHX_0g0stmrX9iyKr480NXONlyWzpERVsdHEr7ORVFrQcymOTvE5llrRPPF2k3my3VRcH5W9vfboDqcy2UuoeeO2oHUcQ3MsLNDkH5dFyHQ4RGE4T2YkE2V7x5QB8Giah0I2h_Zbb49AfCt_GxyQ"}

                    public_key_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jwtRS256.key.pub')
                    public_key = open(public_key_path).read()
                    print("****************************")
                    payload = jwt.decode(access_token, public_key, algorithms=['RS256'])
                    first_name = payload['first_name']
                    last_name = payload['last_name']
                    
                    return HttpResponse(f'You are {first_name} {last_name}')
                else:
                    return HttpResponse("You're not authorized")
            else:
                return HttpResponse("You're not authorized")

    else:
        form = InputForm()
