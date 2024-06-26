from django.shortcuts import render
from django.utils import timezone
from extracciones.models import CitaExtracciones, CurvaLarga
from proxima_cita.forms.forms import ProximaCitaForm
from matrona.models import CitaMatrona
from medicina_familia.models import CitaMedicinaFamilia
from obstetra.models import CitaObstetra
from odontologia.models import CitaOdontologia
from vacuna.models import CitaVacuna
import locale
from datetime import datetime, time
from operator import attrgetter
# Create your views here.

def determinar_tipo(url):
    tipo = None
    if 'test_o_sullivan_curva_larga/' in url:
        tipo = 'test_o_sullivan_curva_larga/'
    elif 'extracciones' in url:
        tipo = 'extracciones'
    elif 'matrona' in url:
        tipo = 'matrona'
    elif 'medicina_familia' in url:
        tipo = 'medicina_familia'
    elif 'obstetra' in url:
        tipo = 'obstetra'
    elif 'odontologia' in url:
        tipo = 'odontologia'
    elif 'vacuna' in url:
        tipo = 'vacuna'
    return tipo



def proxima_cita(request):
    proxima_cita_obj=calcular_proxima_cita(request)
    if proxima_cita_obj is not None:
        especialista = determinar_especialista(proxima_cita_obj)
        fecha_proxima_cita=proxima_cita_obj.fecha
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha=fecha_proxima_cita.strftime("%d de %B de %Y")
        url_proxima_cita=determinar_url_proxima_cita(request,fecha_proxima_cita,especialista)
        initial_data = {
            'fecha': fecha,
            'especialista':especialista,
        }
        form=ProximaCitaForm(initial=initial_data)
        return render(request,'proxima_cita.html',{'form':form,'fecha':fecha,'especialista':especialista,'url_proxima_cita':url_proxima_cita})
    else:
        print('No existe proxima cita.')
        return render(request,'no_hay_citas_pendientes.html')


def determinar_cadena_trimeste(trimestre):
    cadena_trimestre=None
    if trimestre == 1:
        cadena_trimestre='citas_primer'
    elif trimestre == 2:
        cadena_trimestre='citas_segundo'
    elif trimestre == 3:
        cadena_trimestre='citas_tercer'
    return cadena_trimestre

def determinar_cadena_orden(orden):
    cadena_orden=None
    if orden == 1:
        cadena_orden='uno'
    elif orden == 2:
        cadena_orden='dos'
    elif orden == 3:
        cadena_orden='tres'
    return cadena_orden


def determinar_url_proxima_cita(request,fecha_proxima_cita,especialista):
    url_proxima_cita = None
    cadena_trimestre=None
    cadena_orden=None

    if especialista == "Test O'Sullivan Curva Larga":
        cita=CurvaLarga.objects.filter(usuaria=request.user,fecha=fecha_proxima_cita).first()
        cadena_trimestre='citas_segundo'
        especialista='test_o_sullivan_curva_larga'
        url_proxima_cita='/gestion_citas/'+cadena_trimestre+'/extracciones/'+especialista+'/'

    elif especialista == 'Extracciones':
        cita=CitaExtracciones.objects.filter(usuaria=request.user,fecha=fecha_proxima_cita).first()
        cadena_trimestre=determinar_cadena_trimeste(cita.trimestre)
        especialista ='extracciones'
        url_proxima_cita='/gestion_citas/'+cadena_trimestre+'/'+especialista+'/'

    elif especialista == 'Matrona':
        cita=CitaMatrona.objects.filter(usuaria=request.user,fecha=fecha_proxima_cita).first()
        trimestre=cita.trimestre
        cadena_trimestre=determinar_cadena_trimeste(trimestre)
        cadena_orden=determinar_cadena_orden(cita.orden)
        especialista ='matrona'
        if trimestre ==1:
            url_proxima_cita='/gestion_citas/'+cadena_trimestre+'/'+especialista+'/'
        else:
            url_proxima_cita='/gestion_citas/'+cadena_trimestre+'/'+especialista+'/'+cadena_orden+'/'

    elif especialista == 'MedicinaFamilia':
        cita=CitaMedicinaFamilia.objects.filter(usuaria=request.user,fecha=fecha_proxima_cita).first()
        especialista ='medicina_familia'
        cadena_trimestre=determinar_cadena_trimeste(cita.trimestre)
        receta=cita.tipo
        url_proxima_cita='/gestion_citas/'+cadena_trimestre+'/'+especialista+'/'+receta+'/'
       


    elif especialista == 'Obstetra':
        cita=CitaObstetra.objects.filter(usuaria=request.user,fecha=fecha_proxima_cita).first()
        especialista ='obstetra'
        cadena_orden=determinar_cadena_orden(cita.orden)
        trimestre=cita.trimestre
        cadena_trimestre=determinar_cadena_trimeste(cita.trimestre)
        if trimestre==3:
            url_proxima_cita='/gestion_citas/'+cadena_trimestre+'/'+especialista+'/'+cadena_orden+'/'
        else:
            url_proxima_cita='/gestion_citas/'+cadena_trimestre+'/'+especialista+'/'

    elif especialista == 'Odontologia':
        cita=CitaOdontologia.objects.filter(usuaria=request.user,fecha=fecha_proxima_cita).first()
        especialista ='odontologia'
        cadena_trimestre='citas_primer'
        url_proxima_cita='/gestion_citas/'+cadena_trimestre+'/'+especialista+'/'
    

    elif especialista == 'Vacuna':
        cita=CitaVacuna.objects.filter(usuaria=request.user,fecha=fecha_proxima_cita).first()
        especialista ='vacuna'
        nombre=cita.nombre
        if nombre=='gripe':
            url_proxima_cita='/vacunas/gripe/'
        elif nombre == 'tos_ferina':
            url_proxima_cita='/vacunas/tos_ferina/'
            
    return url_proxima_cita



def calcular_proxima_cita(request):
    fecha_actual = timezone.now()
    tipo = None
    proxima_cita=None
    citas=[]
    citas_curva_larga =CurvaLarga.objects.filter(usuaria=request.user)
    citas_extracciones = CitaExtracciones.objects.filter(usuaria=request.user)
    citas_matrona = CitaMatrona.objects.filter(usuaria=request.user)
    citas_medicina_familia = CitaMedicinaFamilia.objects.filter(usuaria=request.user)
    citas_obstetra = CitaObstetra.objects.filter(usuaria=request.user)
    citas_odontologia = CitaOdontologia.objects.filter(usuaria=request.user)
    citas_vacuna = CitaVacuna.objects.filter(usuaria=request.user)
    citas += list(citas_curva_larga)
    citas += list(citas_extracciones)
    citas += list(citas_matrona)
    citas += list(citas_medicina_familia)
    citas += list(citas_obstetra)
    citas += list(citas_odontologia)
    citas += list(citas_vacuna)
    
  
    citas_ordenadas_por_fecha = sorted(citas, key=lambda cita: cita.fecha)

    for cita in citas_ordenadas_por_fecha :
        if cita.fecha >= fecha_actual:
            proxima_cita = cita
            break
    if proxima_cita is not None:
        print(proxima_cita.fecha)
    else:
        print("No hay próxima cita")
    return proxima_cita


def determinar_especialista(proxima_cita):
    tipo=str(type(proxima_cita))
    especialista = None
    if 'CurvaLarga' in tipo:
        especialista="Test O'Sullivan Curva Larga"
    elif 'CitaExtracciones' in tipo:
        especialista = 'Extracciones'
    elif 'CitaMatrona' in tipo:
        especialista = 'Matrona'
    elif 'CitaMedicinaFamilia' in tipo:
        especialista = 'MedicinaFamilia'
    elif 'CitaObstetra' in tipo:
        especialista = 'Obstetra'
    elif 'CitaOdontologia' in tipo:
        especialista = 'Odontologia'
    elif 'CitaVacuna' in tipo:
        especialista = 'Vacuna'
    return especialista

