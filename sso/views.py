from django.http import HttpResponse
import requests
import json

def index(request):
    url = 'https://api.testable.io/'
    print("************************")
    print(requests.get(url).json())
    print("************************")
    response = requests.get(url).json()

    return HttpResponse("You're %s." % response['name'])