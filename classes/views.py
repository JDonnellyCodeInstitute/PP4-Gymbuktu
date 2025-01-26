from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def classes_test(request):
    return HttpResponse("Hello, World!")