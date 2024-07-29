from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



# @method_decorator(ensure_csrf_cookie, name='dispatch')
def LoginPage(request):
    return render(request, 'login.html')

# @login_required
def Dashboard(request):
    return render(request,'dashboard.html')

def login_again(request):
    return render(request,'login_again.html')


def profilePage(request):
    return render(request, 'profile.html')


@login_required
def check_session(request):
    return JsonResponse({'status': 'ok'})
