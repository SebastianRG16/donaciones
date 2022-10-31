from email import message
from http.client import HTTPResponse
from multiprocessing import AuthenticationError
from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Asistente, Preregistro
import qrcode
import qrcode.image.svg
from io import BytesIO
import cv2
import numpy as np
from django.contrib import messages

# from mainSistema.models import Asistente
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
    datosRegistros = Asistente.objects.all().values('idAsistente', 'nombres', 'apellidos', 'documento', 'telefono', 'correo', 'tipo_aporte', 'tipo_persona')
    return render(request,"registro.html",{   
        'mostrarRegistros' : datosRegistros,
})

@login_required
def salir(request):
    logout(request)
    return redirect('ingresar')


def preRegistro(request):
    datospreRegistro = Asistente.objects.all().values('idAsistente', 'nombres', 'apellidos', 'documento', 'telefono', 'correo')
    

    return render(request, 'preRegistro.html',{
       'mostrarpreRegistro' : datospreRegistro, 
    })

@login_required
def save_tareas(request):
    
    if request.method == 'POST':
        nombres = request.POST["nombres"]
        apellidos = request.POST["apellidos"]
        documento = request.POST["documento"]
        telefono = request.POST["telefono"]
        correo = request.POST["correo"]
        tipo_aporte = request.POST["tipo_aporte"]
        tipo_persona = request.POST["tipo_persona"]
        



        Asis = Asistente(

            nombres = nombres,
            apellidos = apellidos,
            documento = documento,
            telefono = telefono,
            correo = correo,
            tipo_aporte = tipo_aporte,
            tipo_persona = tipo_persona


        )
        Asis.save()

        


        return redirect("tareas")
    
    else:
        return redirect("registro")


def save_preRegistro(request):

    if request.method == 'POST':
        nombres = request.POST["nombres"]
        apellidos = request.POST["apellidos"]
        documento = request.POST["documento"]
        telefono = request.POST["telefono"]
        correo = request.POST["correo"]
        



        Asis = Preregistro(

            nombres = nombres,
            apellidos = apellidos,
            documento = documento,
            telefono = telefono,
            correo = correo,
        )
        Asis.save()
    
    try:
        Asistente.objects.filter(documento = Asis.documento)
        messages.warning(request, 'El asistente ya existe')
    except:
        messages.success(request, 'Se guardo correctamente')




    context = {}
    if request.method == "POST":
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(request.POST.get("documento",""), image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()

    return render(request, "preRegistro.html", context=context)


@login_required
def leerqr(request):

    capture = cv2.VideoCapture(0)
    while(capture.isOpened()):
        ret, frame = capture.read()
        if (cv2.waitKey(1) == ord('s')):
            break
        qrDetector = cv2.QRCodeDetector()
        data, bbox, rectifiedImage = qrDetector.detectAndDecode(frame)

        if len (data) > 0:
            print({data})
            cv2.imshow('webCam', rectifiedImage)
            capture.release()
        else: 
            cv2.imshow('webCam', frame)
    
    capture.release()
    cv2.destroyAllWindows

    qrDocumento = data

    print({qrDocumento})

    datosRegistros = Asistente.objects.get(documento = qrDocumento)
    

    return render(request, 'autoInfo.html', {
        'mostraDocumento' : qrDocumento,
        'validoDocumento' : datosRegistros, 
    })

#  .\venv\Scripts\activate

# python -m venv venv