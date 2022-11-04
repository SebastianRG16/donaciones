from email import message
from http.client import HTTPResponse
from multiprocessing import AuthenticationError
from urllib import response
from multiprocessing import AuthenticationError, context
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

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
            'error': 'el usuario o la contraseña son incorrectos'
        })
        else:
            login(request, user)
            return redirect('tareas')


@login_required
def tareas(request):
    return render(request, 'tareas.html')


@login_required
def registro(request):
    datosRegistros = Asistente.objects.all().values('idAsistente', 'nombres',
                                           'apellidos', 'documento', 'telefono', 'correo', 'tipo_aporte', 'tipo_persona')
    return render(request, "registro.html", {
        'mostrarRegistros': datosRegistros,
})


@login_required
def salir(request):
    logout(request)
    return redirect('ingresar')


def preRegistro(request):
    datospreRegistro = Asistente.objects.all().values(
        'idAsistente', 'nombres', 'apellidos', 'documento', 'telefono', 'correo')

    return render(request, 'preRegistro.html', {
       'mostrarpreRegistro': datospreRegistro,
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

            nombres=nombres,
            apellidos=apellidos,
            documento=documento,
            telefono=telefono,
            correo=correo,
            tipo_aporte=tipo_aporte,
            tipo_persona=tipo_persona
        )
        Asis.save()
        messages.success(request, 'Ingreso registrado de manera correcta.')

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
            nombres=nombres,
            apellidos=apellidos,
            documento=documento,
            telefono=telefono,
            correo=correo,
        )

    context = {}

    try:
        guardar = Asis.documento
        datosRegistros = Asistente.objects.get(documento=guardar)
        print(datosRegistros.documento)
        messages.warning(request, 'El asistente ya existe')
    except:
        messages.success(request, 'Se guardo correctamente')
        Asis.save()
        messages.success(
            request, 'Has sido registrado en el evento de manera correcta.')
    return redirect("preRegistro")


def qr_ingreso(request):
    context = {}
    try:

        if request.method == "POST":
            documento = request.POST["documento"]
            preRegistro = Preregistro.objects.get(documento=documento)

            factory = qrcode.image.svg.SvgImage
            img = qrcode.make(request.POST.get("documento", ""),
                              image_factory=factory, box_size=20)
            stream = BytesIO()
            img.save(stream)
            context["svg"] = stream.getvalue().decode()

        return render(request, 'qrIngreso.html', context=context)
    except ObjectDoesNotExist:
        messages.warning(request, 'No estás registrado.')
        return render(request, 'qrIngreso.html', context=context)   
    


@login_required
def leerqr(request):
    x_form_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_form_for is not None:
        ip = x_form_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    print(f"ip= {ip}")
    
    if ip == '192.168.1.100':
        n = 1
    elif ip == '192.168.1.103':
        n = 2

    capture = cv2.VideoCapture(n)
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

    print(qrDocumento)

    registro = Preregistro.objects.get(documento = qrDocumento)
    messages.success(request, 'Ingreso de invitado ha sido guardado.')
    

    return render(request, 'autoInfo.html', {
        'mostraDocumento' : qrDocumento,
        'registro' : registro, 
    })

@login_required
def Resumen(request):
    totalRegistrados = Asistente.objects.all().values('idAsistente')
    i=0
    for total1 in totalRegistrados:
        i=i+1
    finalRegistrados = i

    totaltpersona = Asistente.objects.all().values('tipo_persona')
    
    j=0
    k=0

    for total2 in totaltpersona:
        print(total2) 
        
        if total2 == {'tipo_persona': 'Asistente'}:
            j=j+1
            print(j)
        elif total2 == {'tipo_persona': 'Invitado especial'}:
            k=k+1
            print(k)

    totalAsistentes = j
    totalInvitadoespecial = k

    return render(request, 'Resumen.html',{
        'registrados' : finalRegistrados, 
        'asistentes' : totalAsistentes,
        'Invitadoespecial' : totalInvitadoespecial,
    })


#  .\venv\Scripts\activate

# python -m venv venv