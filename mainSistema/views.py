from email import message
from http.client import HTTPResponse
from multiprocessing import AuthenticationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def ingresar(request):
    if request.method == 'GET':
        return render(request, 'ingresar.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ingresar.html', {
            'form': AuthenticationForm,
            'error':'el usuario o la contraseña son incorrectos'
        })
        else:
            login(request, user)
            return redirect('tareas')

@login_required
def tareas(request):
    return render(request, 'tareas.html')

@login_required
def registro(request):
    return render(request, 'registro.html')

@login_required
def salir(request):
    logout(request)
    return redirect('ingresar')

#  .\venv\Scripts\activate

# python -m venv venv
