from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
#def child1(request):
    #return render(request, 'base.html')

def trangchu(request):
    return render(request, 'base.html')

def child1(request):
    return render(request, 'child1.html')

def child2(request):
    return render(request, 'child2.html')

def child3(request):
    return render(request, 'child3.html')

def minigames(request):
    return render(request, 'minigames.html')
