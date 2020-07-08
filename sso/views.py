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
            
            b64credentials = base64.b64encode(f'{login}:{password}'.encode()).decode()
            response1 = requests.post('https://consplusweb-dev:8097/backend/oauth/code/user?client_id=test', headers={'Authorization': f'Basic {b64credentials}'}, verify=False).json()
            if 'code' in response1:
                code = response1['code']

                b64secret = base64.b64encode(f'test:secret'.encode()).decode()
                
                response2 = requests.post(f'https://consplusweb-dev:8097/backend/oauth/code/client?code={code}', headers={'Authorization': f'Basic {b64secret}'}, verify=False).json()
                if 'access_token' in response2:
                    access_token = response2['access_token']
                    public_key_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jwtRS256.key.pub')
                    public_key = open(public_key_path).read()
                    
                    payload = jwt.decode(access_token, public_key, algorithms=['RS256'])
                    first_name = payload['first_name']
                    last_name = payload['last_name']
                    return HttpResponse(f'You are {first_name} {last_name}')
                else:
                    return HttpResponse("Invalid username or password")
            else:
                return HttpResponse("Invalid username or password")
    else:
        form = InputForm()
