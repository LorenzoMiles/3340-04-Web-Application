from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(response, id):
    return render(response, "SEApp/base.html", {})

def home(response):
    return render(response, "SEApp/home.html", {})
