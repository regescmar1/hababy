from django.shortcuts import render,redirect
from .forms.forms import CitaExtraccionesForm, CurvaLargaForm
from extracciones.models import CitaExtracciones, CurvaLarga
from django.contrib.auth.decorators import login_required

def determinar_trimestre(url):
    trimestre = None
    if 'citas_primer' in url:
        trimestre = 1
    elif 'citas_segundo' in url:
        trimestre = 2
    elif 'citas_tercer' in url:
        trimestre = 3
    return trimestre

@login_required
def ver_archivos(request):
    return render(request,'ver_archivos.html')

@login_required
def mostrar_formulario(request):
    url=request.path
    trimestre = determinar_trimestre(url)
    cita_existente = CitaExtracciones.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    fecha_cita = cita_existente.fecha if cita_existente else None
    initial_data = {
        'fecha': fecha_cita,
        'analisis_normal': cita_existente.analisis_normal if cita_existente else None,
        'test_o_sullivan_positivo': cita_existente.test_o_sullivan_positivo if cita_existente else None,
        'rh_negativo': cita_existente.rh_negativo if cita_existente else None,
        'anemia': cita_existente.anemia if cita_existente else None,
        'observaciones':cita_existente.observaciones if cita_existente else None,
    }
    if cita_existente and trimestre == 2:
        test_o_sullivan_positivo=cita_existente.test_o_sullivan_positivo
        form = CitaExtraccionesForm(initial=initial_data)
        return render(request, 'extracciones.html', {'form': form,'trimestre':trimestre,'cita_existente':cita_existente,
                                                     'test_o_sullivan_positivo':test_o_sullivan_positivo})
    else:
        form = CitaExtraccionesForm(initial=initial_data)
        return render(request, 'extracciones.html', {'form': form,'trimestre':trimestre,'cita_existente':cita_existente})

@login_required
def eliminar_cita_extracciones(request):
    url = request.path
    trimestre = determinar_trimestre(url)
    print(trimestre)
    form = CitaExtraccionesForm(request.POST or None)
    if request.method == 'POST':
        cita_existente = CitaExtracciones.objects.filter(usuaria=request.user, trimestre=trimestre).first()
        if cita_existente:
            cita_existente.delete()
        if trimestre==1:
            return redirect('/gestion_citas/citas_primer/')
        elif trimestre==2:
            return redirect('/gestion_citas/citas_segundo/')
        elif trimestre==3:
            return redirect('/gestion_citas/citas_tercer/')
    return render(request, 'eliminar_cita_extracciones.html',{'form':form,'trimestre':trimestre})

@login_required
def extracciones(request):
    url = request.path
    trimestre = determinar_trimestre(url)
    form = CitaExtraccionesForm(request.POST or None)
    if request.method == 'POST':
        form = CitaExtraccionesForm(request.POST, request.FILES)
        print('formulario valido',form.is_valid())
        if form.is_valid():
            return crear_actualizar_cita_extracciones(request,form)
        else:
            print(form.errors)
    else:
        return mostrar_formulario(request)
    return render(request, 'extracciones.html', {'form': form,'trimestre':trimestre})

@login_required
def crear_actualizar_cita_extracciones(request,form):
    url = request.path
    trimestre = determinar_trimestre(url)
    test_o_sullivan_positivo=False
    cita_existente=CitaExtracciones.objects.filter(usuaria=request.user,trimestre=trimestre).first()
    if cita_existente:
        cita_existente.fecha = form.cleaned_data['fecha']
        cita_existente.analisis_normal = form.cleaned_data['analisis_normal']
        cita_existente.test_o_sullivan_positivo = form.cleaned_data['test_o_sullivan_positivo']
        cita_existente.rh_negativo = form.cleaned_data['rh_negativo']
        cita_existente.anemia = form.cleaned_data['anemia']
        cita_existente.observaciones = form.cleaned_data['observaciones']
        cita_existente.save()
        test_o_sullivan_positivo=cita_existente.test_o_sullivan_positivo
    else:
        nueva_cita = CitaExtracciones.objects.create(
            fecha=form.cleaned_data['fecha'],
            analisis_normal=form.cleaned_data['analisis_normal'],
            test_o_sullivan_positivo=form.cleaned_data['test_o_sullivan_positivo'],
            rh_negativo=form.cleaned_data['rh_negativo'],
            anemia=form.cleaned_data['anemia'],
            observaciones=form.cleaned_data['observaciones'],
            trimestre=trimestre,
            usuaria=request.user
        )
        test_o_sullivan_positivo=nueva_cita.test_o_sullivan_positivo
        nueva_cita.save()
    return render(request, 'extracciones.html', {'form': form,'trimestre':trimestre,'test_o_sullivan_positivo':test_o_sullivan_positivo})

@login_required
def test_o_sullivan_curva_larga(request):
    url = request.path
    trimestre=determinar_trimestre(url)
    form = CurvaLargaForm(request.POST or None)
    if request.method == 'POST':
        form = CitaExtraccionesForm(request.POST, request.FILES)
        print('formulario valido',form.is_valid())
        if form.is_valid():
            return crear_actualizar_cita_test_o_sullivan_curva_larga(request,form)
        else:
            print(form.errors)
    else:
        return mostrar_formulario_test_o_sullivan_curva_larga(request)
    return render(request, 'test_o_sullivan_curva_larga.html',{'form': form,'trimestre':trimestre})

@login_required
def mostrar_formulario_test_o_sullivan_curva_larga(request):
    cita_existente = CurvaLarga.objects.filter(usuaria=request.user, trimestre=2).first()
    fecha_cita = cita_existente.fecha if cita_existente else None
    initial_data = {
        'fecha': fecha_cita,
        'analisis_normal': cita_existente.analisis_normal if cita_existente else None,
        'observaciones':cita_existente.observaciones if cita_existente else None,
    }
    form = CurvaLargaForm(initial=initial_data)
    return render(request, 'test_o_sullivan_curva_larga.html', {'form': form,'cita_existente':cita_existente})

@login_required
def crear_actualizar_cita_test_o_sullivan_curva_larga(request,form):
    url = request.path
    trimestre=determinar_trimestre(url)
    cita_existente=CurvaLarga.objects.filter(usuaria=request.user,trimestre=2).first()
    if cita_existente:
        cita_existente.fecha = form.cleaned_data['fecha']
        cita_existente.analisis_normal = form.cleaned_data['analisis_normal']
        cita_existente.observaciones = form.cleaned_data['observaciones']
        cita_existente.save()
    else:
        nueva_cita = CurvaLarga.objects.create(
            fecha=form.cleaned_data['fecha'],
            analisis_normal=form.cleaned_data['analisis_normal'],
            observaciones=form.cleaned_data['observaciones'],
            trimestre=trimestre,
            usuaria=request.user
        )
        nueva_cita.save()
    return render(request, 'test_o_sullivan_curva_larga.html', {'form': form,'trimestre':trimestre})

@login_required
def eliminar_cita_test_o_sullivan_curva_larga(request):
    url = request.path
    trimestre = determinar_trimestre(url)
    form = CurvaLargaForm(request.POST or None)
    if request.method == 'POST':
        cita_existente = CurvaLarga.objects.filter(usuaria=request.user, trimestre=trimestre).first()
        if cita_existente:
            cita_existente.delete()
            return redirect('/gestion_citas/citas_segundo/extracciones/')
    return render(request, 'eliminar_cita_test_o_sullivan_curva_larga.html',{'form':form,'trimestre':trimestre})