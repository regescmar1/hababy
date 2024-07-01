

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from extracciones.models import CitaExtracciones, CurvaLarga
from archivo.models import ArchivoCurvaLarga, ArchivoExtracciones,ArchivoObstetra
from archivo.forms.forms import  ArchivoForm
from extracciones.forms.forms import CitaExtraccionesForm, CurvaLargaForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from obstetra.models import CitaObstetra
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image



from obstetra.forms.forms import CitaObstetraForm



def determinar_trimestre(url):
    trimestre = None
    if 'citas_primer' in url:
        trimestre = 1
    elif 'citas_segundo' in url:
        trimestre = 2
    elif 'citas_tercer' in url:
        trimestre = 3
    return trimestre

def determinar_orden(url):
    orden=None
    if 'uno' in url:
        orden = 1
    elif 'dos' in url:
        orden = 2
    elif 'tres' in url:
        orden = 3
    return orden

def determinar_tipo(url):
    tipo = None
    if 'curva_larga' in url:
        tipo = 'curva_larga'
    elif 'obstetra' in url:
        tipo = 'obstetra'
    elif 'extracciones' in url:
        tipo= 'extracciones'
    return tipo


@login_required
def archivo(request):
    url = request.path
    print(url)
    trimestre = determinar_trimestre(url)
    orden=determinar_orden(url)
    print('orden',orden)
    tipo=determinar_tipo(url)
    cita_existente=None
    if tipo=='curva_larga':
        print(tipo)
        form = CurvaLargaForm(request.POST or None)
        cita_existente=CurvaLarga.objects.filter(usuaria=request.user,trimestre=trimestre).first()
    elif tipo=='extracciones':
        form = CitaExtraccionesForm(request.POST or None)
        cita_existente = CitaExtracciones.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    elif tipo=='obstetra':
        form = CitaObstetraForm(request.POST or None)
        cita_existente = CitaObstetra.objects.filter(usuaria=request.user, trimestre=trimestre,orden=orden).first()

    if request.method == 'POST':
        print('ispost')
        form = ArchivoForm(request.POST, request.FILES)
        print('formulario valido',form.is_valid())
        if form.is_valid():
            if (tipo=='curva_larga'):
                return crear_archivo_curva_larga(request,form)
            elif (tipo=='extracciones'):
                return crear_archivo_extracciones(request,form)
            elif (tipo=='obstetra'):
                return crear_archivo_obstetra(request,form)
        else:
            print(form.errors)
            return render(request,'error_formato.html',{'form':form})
    else:
        if tipo=='curva_larga':
            return mostrar_listado_archivo_curva_larga(request,trimestre)
        elif tipo=='extracciones':
            return mostrar_listado_archivo_extracciones(request,trimestre)
        elif tipo=='obstetra':
            return mostrar_listado_archivo_obstetra(request,trimestre,orden)
    if (tipo=='curva_larga'):
        return render(request, 'archivos_curva_larga.html', {'form': form,'trimestre':trimestre,'cita_existente':cita_existente})
    elif (tipo=='obstetra'):
        return render(request, 'archivos_obstetra.html', {'form': form,'trimestre':trimestre,'orden':orden,'cita_existente':cita_existente})
    elif (tipo=='extracciones'):
        return render(request, 'archivos_extracciones.html', {'form': form,'trimestre':trimestre,'cita_existente':cita_existente})


@login_required
def mostrar_listado_archivo_extracciones(request,trimestre):
    cita_existente = CitaExtracciones.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    archivos_extracciones_existentes = ArchivoExtracciones.objects.filter(usuaria=request.user, cita_extracciones=cita_existente)
    return render(request, 'archivos_extracciones.html', {'archivos_extracciones_existentes':archivos_extracciones_existentes,
                                                          'trimestre':trimestre,'cita_existente':cita_existente})

@login_required
def mostrar_listado_archivo_obstetra(request,trimestre,orden):
    if (orden is None):
        cita_existente = CitaObstetra.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    else:
        cita_existente = CitaObstetra.objects.filter(usuaria=request.user, trimestre=trimestre,orden=orden).first()
    archivos_obstetra_existentes = []
    if cita_existente:
        archivos_obstetra_existentes = ArchivoObstetra.objects.filter(usuaria=request.user, cita_obstetra=cita_existente)

    return render(request, 'archivos_obstetra.html', {'archivos_obstetra_existentes': archivos_obstetra_existentes,
                                                      'trimestre': trimestre, 'orden': orden, 'cita_existente': cita_existente})

@login_required
def mostrar_listado_archivo_curva_larga(request,trimestre):
    cita_existente = CurvaLarga.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    archivos_curva_larga_existentes = ArchivoCurvaLarga.objects.filter(usuaria=request.user, cita_curva_larga=cita_existente)
    return render(request, 'archivos_curva_larga.html', {'archivos_curva_larga_existentes':archivos_curva_larga_existentes,
                                                         'trimestre':trimestre,'cita_existente':cita_existente})

@login_required
def crear_archivo_extracciones(request,form):
    url = request.path
    trimestre = determinar_trimestre(url)
    cita_existente=CitaExtracciones.objects.filter(usuaria=request.user,trimestre=trimestre).first()
    nuevo_archivo = ArchivoExtracciones.objects.create(
        archivo=form.cleaned_data['archivo'],
        cita_extracciones=cita_existente,
        usuaria=request.user
    )
    nuevo_archivo.save()
    if trimestre == 1:
        return redirect('/gestion_citas/citas_primer/extracciones/archivos/archivo_guardado_con_exito/')
    elif trimestre == 2:
        return redirect('/gestion_citas/citas_segundo/extracciones/archivos/archivo_guardado_con_exito/')
    elif trimestre == 3:
        return redirect('/gestion_citas/citas_tercer/extracciones/archivos/archivo_guardado_con_exito/')

@login_required
def crear_archivo_curva_larga(request,form):
    url = request.path
    trimestre = determinar_trimestre(url)
    cita_existente=CurvaLarga.objects.filter(usuaria=request.user,trimestre=trimestre).first()
    nuevo_archivo = ArchivoCurvaLarga.objects.create(
        archivo=form.cleaned_data['archivo'],
        cita_curva_larga=cita_existente,
        usuaria=request.user
    )
    nuevo_archivo.save()
    return redirect('/gestion_citas/citas_segundo/extracciones/test_o_sullivan_curva_larga/archivos/archivo_guardado_con_exito/')

@login_required
def crear_archivo_obstetra(request,form):
    print(form)
    url = request.path
    trimestre = determinar_trimestre(url)
    orden=determinar_orden(url)
    if (orden==None):
        cita_existente = CitaObstetra.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    else:
        cita_existente = CitaObstetra.objects.filter(usuaria=request.user, trimestre=trimestre,orden=orden).first()
    nuevo_archivo = ArchivoObstetra.objects.create(
        archivo=form.cleaned_data['archivo'],
        cita_obstetra=cita_existente,
        usuaria=request.user
    )
    nuevo_archivo.save()
    if trimestre == 1:
        return redirect('/gestion_citas/citas_primer/obstetra/archivos/archivo_guardado_con_exito/')
    elif trimestre == 2:
        return redirect('/gestion_citas/citas_segundo/obstetra/archivos/archivo_guardado_con_exito/')
    elif trimestre == 3 and orden == 1:
        return redirect('/gestion_citas/citas_tercer/obstetra/uno/archivos/archivo_guardado_con_exito/')
    elif trimestre == 3 and orden == 2:
        return redirect('/gestion_citas/citas_tercer/obstetra/dos/archivos/archivo_guardado_con_exito/')
    elif trimestre == 3 and orden == 3:
        return redirect('/gestion_citas/citas_tercer/obstetra/tres/archivos/archivo_guardado_con_exito/')

@login_required
def archivo_guardado_con_exito(request):
    url = request.path
    trimestre = determinar_trimestre(url)
    orden=determinar_orden(url)
    tipo=determinar_tipo(url)
    return render(request, 'archivo_guardado_con_exito.html' ,{'trimestre':trimestre,'orden':orden,'tipo':tipo})

@login_required
def ver_archivo(request, archivo_id):
    url = request.path
    tipo= determinar_tipo(url)
    if tipo == 'curva_larga':
        archivo = get_object_or_404(ArchivoCurvaLarga, pk=archivo_id)
    elif tipo == 'extracciones':
        archivo = get_object_or_404(ArchivoExtracciones, pk=archivo_id)
    elif tipo == 'obstetra':
        archivo = get_object_or_404(ArchivoObstetra, pk=archivo_id)
    return render(request, 'ver_archivo.html', {'archivo': archivo})

@login_required
def descargar_archivo(request,archivo_id):
    url = request.path
    tipo= determinar_tipo(url)
    if tipo == 'curva_larga':
        archivo = get_object_or_404(ArchivoCurvaLarga, pk=archivo_id)
    elif tipo == 'extracciones':
        archivo = get_object_or_404(ArchivoExtracciones, pk=archivo_id)
    elif tipo == 'obstetra':
        archivo = get_object_or_404(ArchivoObstetra, pk=archivo_id)
    ruta_archivo = archivo.archivo.path
    print(ruta_archivo)
    try:
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()
        return HttpResponse(contenido, content_type='application/octet-stream')
    except FileNotFoundError:
        return HttpResponse("El archivo no se encontró", status=404)

@login_required
def eliminar_archivo(request, archivo_id):
    print(archivo_id)
    url = request.path
    trimestre=determinar_trimestre(url)
    orden=determinar_orden(url)
    tipo= determinar_tipo(url)
    if tipo == 'curva_larga':
        archivo = get_object_or_404(ArchivoCurvaLarga, pk=archivo_id)
    elif tipo == 'extracciones':
        archivo = get_object_or_404(ArchivoExtracciones, pk=archivo_id)
    elif tipo == 'obstetra':
        archivo = get_object_or_404(ArchivoObstetra, pk=archivo_id)
    archivo.delete()
    if tipo=='curva_larga':
        return redirect('/gestion_citas/citas_segundo/extracciones/test_o_sullivan_curva_larga/archivos/archivo_eliminado/')
    elif trimestre==1 and tipo=='extracciones':
        return redirect('/gestion_citas/citas_primer/extracciones/archivos/archivo_eliminado/')
    elif trimestre==2 and tipo=='extracciones':
        return redirect('/gestion_citas/citas_segundo/extracciones/archivos/archivo_eliminado/')
    elif trimestre==3 and tipo=='extracciones':
        return redirect('/gestion_citas/citas_tercer/extracciones/archivos/archivo_eliminado/')
    elif trimestre==1 and tipo=='obstetra':
        return redirect('/gestion_citas/citas_primer/obstetra/archivos/archivo_eliminado/')
    elif trimestre==2 and tipo=='obstetra':
        return redirect('/gestion_citas/citas_segundo/obstetra/archivos/archivo_eliminado/')
    elif trimestre==3 and orden==1 and tipo=='obstetra':
        return redirect('/gestion_citas/citas_tercer/obstetra/uno/archivos/archivo_eliminado/')
    elif trimestre==3 and orden==2 and tipo=='obstetra':
        return redirect('/gestion_citas/citas_tercer/obstetra/dos/archivos/archivo_eliminado/')
    elif trimestre==3 and orden==3 and tipo=='obstetra':
        return redirect('/gestion_citas/citas_tercer/obstetra/tres/archivos/archivo_eliminado/')

@login_required
def archivo_eliminado(request):
    url = request.path
    trimestre = determinar_trimestre(url)
    tipo=determinar_tipo(url)
    orden=determinar_orden(url)
    return render(request, 'archivo_eliminado.html',{'trimestre':trimestre,'orden':orden,'tipo':tipo})

@login_required
def generar_pdf(request):
    url=request.path
    trimestre=determinar_trimestre(url)
    orden=determinar_orden(url)
    tipo=determinar_tipo(url)
    if tipo=='curva_larga':
        archivos=ArchivoCurvaLarga.objects.filter(usuaria=request.user,cita_curva_larga__trimestre=trimestre)
    elif tipo=='obstetra':
        if (orden is None):
            archivos=ArchivoObstetra.objects.filter(usuaria=request.user,cita_obstetra__trimestre=trimestre)
        else:
            archivos=ArchivoObstetra.objects.filter(usuaria=request.user,cita_obstetra__trimestre=trimestre,cita_obstetra__orden=orden)
    elif tipo=='extracciones':
        archivos= ArchivoExtracciones.objects.filter(usuaria=request.user, cita_extracciones__trimestre=trimestre)
    response = HttpResponse(content_type='application/pdf')
    filename = "listado_archivos_extracciones.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    for archivo in archivos:
        imagen_path = archivo.archivo.path
        img = Image(imagen_path, width=400, height=400)
        elements.append(img)
    doc.build(elements)
    return response