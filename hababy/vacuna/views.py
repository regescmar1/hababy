from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from extracciones.models import CitaExtracciones
from vacuna.models import CitaVacuna
from .forms.forms import CitaVacunaForm

# Create your views here.
@login_required
def vacunas(request):
    cita_extracciones_segundo=CitaExtracciones.objects.filter(usuaria=request.user, trimestre=2).first()
    antid=False
    if cita_extracciones_segundo:
        if cita_extracciones_segundo.rh_negativo:
            antid=True
    return render(request, 'vacunas.html', {'antid':antid})


def determinar_nombre(url):
    nombre = None
    if 'gripe' in url:
        nombre = 'gripe'
    elif 'tos_ferina' in url:
        nombre = 'tos_ferina'
    elif 'antid' in url:
        nombre = 'antid'
    return nombre


@login_required
def vacuna(request):
    url = request.path
    nombre=determinar_nombre(url)
    form = CitaVacunaForm(request.POST or None)
    cita_existente = CitaVacuna.objects.filter(usuaria=request.user,nombre=nombre).first()
    if request.method == 'POST':
        form = CitaVacunaForm(request.POST, request.FILES)
        print('formulario valido',form.is_valid())
        if form.is_valid():
            return crear_actualizar_cita_vacuna(request,form)
        else:
            print(form.errors)
    else:
        return mostrar_formulario(request)
    return render(request, 'vacuna.html', {'form': form,'nombre':nombre})


@login_required
def mostrar_formulario(request):
    url=request.path
    nombre=determinar_nombre(url)
    cita_existente = CitaVacuna.objects.filter(usuaria=request.user,nombre=nombre).first()
    fecha_cita = cita_existente.fecha if cita_existente else None
    initial_data = {
        'fecha': fecha_cita,
        'nombre': cita_existente.nombre if cita_existente else None,
        'observaciones':cita_existente.observaciones if cita_existente else None,
    }
    form = CitaVacunaForm(initial=initial_data)
    return render(request, 'vacuna.html', {'form': form,'cita_existente':cita_existente,'nombre':nombre})


@login_required
def crear_actualizar_cita_vacuna(request,form):
    url = request.path
    nombre = determinar_nombre(url)
    cita_existente = CitaVacuna.objects.filter(usuaria=request.user,nombre=nombre).first()
    if cita_existente:
        print('0')
        cita_existente.fecha = form.cleaned_data['fecha']
        cita_existente.nombre = nombre
        cita_existente.observaciones = form.cleaned_data['observaciones']
        cita_existente.save()
    else:
        print('1') 
        nueva_cita = CitaVacuna.objects.create(
            fecha=form.cleaned_data['fecha'],
            nombre=nombre,
            observaciones=form.cleaned_data['observaciones'],
            usuaria=request.user
        )
        nueva_cita.save()
    return render(request, 'vacuna.html', {'form': form,'nombre':nombre})


@login_required
def eliminar_cita_vacuna(request):
    url = request.path
    nombre = determinar_nombre(url)
    print(nombre)
    form = CitaVacunaForm(request.POST or None)
    if request.method == 'POST':
        cita_existente = CitaVacuna.objects.filter(usuaria=request.user, nombre=nombre).first()
        if cita_existente:
            cita_existente.delete()

        return redirect('/vacunas/')
       
    return render(request, 'eliminar_cita_vacuna.html',{'form':form,'nombre':nombre})
    