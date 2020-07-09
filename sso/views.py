import base64
import os
import requests
import jwt
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


def login(request):
    """Checks whether cookie with access_token exists.
    If no, user will be redirected to login form
    """
    access_token = request.COOKIES.get('access_token')
    redirect_url = f'https://consplusweb-dev:8097/login?client_id=test&redirect_url=http:%2F%2F{os.environ["DEMO_ENDPOINT"]}/authorize'

    if not access_token:
        return redirect(redirect_url)

    public_key_path = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        'jwtRS256.key.pub')
    public_key = open(public_key_path).read()

    try:
        payload = jwt.decode(
            access_token, public_key, algorithms=['RS256'])
        context = {
            'first_name': payload['first_name'],
            'last_name': payload['last_name']}
        return render(request, 'authorized.html', context)
    except jwt.ExpiredSignatureError:
        return redirect(redirect_url)
    except jwt.DecodeError:
        return redirect('/error')


def authorize(request):
    """Calls sso service to get JWT token
    If token is correct, user will be authenticated.
    In the other case, error page will be shown
    """
    auth_code = request.GET['auth_code']

    if auth_code:
        b64secret = base64.b64encode('test:secret'.encode()).decode()

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

        return redirect('/error')

    return redirect('/error')


def error(request):
    '''Redirects user to error page'''
    context = {'error_message': 'An error has occurred!'}
    return render(request, 'error.html', context)
