from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
import base64
import json
import jwt
import os


def login(request):
    access_token = request.COOKIES.get('access_token')

    if not access_token:
        return redirect("https://consplusweb-dev:8097/login?client_id=test&redirect_url=http:%2F%2Flocalhost:8000/authorize")
    else:
        public_key_path = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)),
            'jwtRS256.key.pub')
        public_key = open(public_key_path).read()

        try:
            payload = jwt.decode(
                access_token, public_key, algorithms=['RS256'])
            context = {'first_name': payload['first_name'], 'last_name': payload['last_name']}
            return render(request, 'authorized.html', context)
        except jwt.ExpiredSignatureError:
            return redirect("https://consplusweb-dev:8097/login?client_id=test&redirect_url=http:%2F%2Flocalhost:8000/authorize")
        except jwt.DecodeError:
            return redirect('/error')

def authorize(request):
    auth_code = request.GET['auth_code']

    if auth_code:
        b64secret = base64.b64encode(f'test:secret'.encode()).decode()

        response = requests.post(
            f'https://consplusweb-dev:8097/backend/oauth/code/client?code={auth_code}',
            headers={
                'Authorization': f'Basic {b64secret}'},
            verify=False).json()

        if 'access_token' in response:
            access_token = response['access_token']
            response = HttpResponseRedirect('/')
            response.set_cookie('access_token', access_token)

            return response
        else:
            return redirect('/error')

    else:
        return redirect('/error')

def error(request):
    context = {'error_message': 'An error has occurred!'}
    return render(request, 'error.html', context)
