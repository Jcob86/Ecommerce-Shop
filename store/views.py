from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response

def example(request):
    return HttpResponse('ok')

