from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def gym_goers_test(request):
    return HttpResponse("Hello, World!")