from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def child1(request):
    return render(request, 'base.html')

def hello(request):
    return JsonResponse({"message": "Xin chào từ Django!"})