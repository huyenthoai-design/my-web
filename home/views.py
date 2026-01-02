from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
#def child1(request):
    #return render(request, 'base.html')

def base(request):
    return render(request, 'base.html')

def trangchu(request):
    return render(request, 'trangchu.html')

def gioithieu(request):
    return render(request, 'gioithieu.html')

def lienhe(request):
    return render(request, 'lienhe.html')

def minigames(request):
    return render(request, 'minigames.html')

def monhoc(request):
    return render(request, 'monhoc.html')

def sinhhoc(request):
    return render(request, 'sinhhoc.html')
