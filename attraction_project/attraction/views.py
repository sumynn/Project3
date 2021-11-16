from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'attraction/index.html')


def attraction_page(request):
    return render(request, 'attraction/attraction.html')


def map_page(request):
    return render(request, 'attraction/eu_map.html')
