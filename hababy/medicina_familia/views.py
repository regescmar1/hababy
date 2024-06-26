from django.shortcuts import render,redirect

from extracciones.models import CitaExtracciones
from .forms.forms import CitaMedicinaFamiliaForm
from medicina_familia.models import CitaMedicinaFamilia
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

def determinar_tipo(url):
    tipo = None
    if 'acido_folico' in url:
        tipo = 'acido_folico'
    elif 'hierro' in url:
        tipo = 'hierro'
    return tipo

@login_required
def mostrar_formulario_hierro(request):
    url=request.path
    trimestre = determinar_trimestre(url)
    tipo=determinar_tipo(url)
    cita_existente = CitaMedicinaFamilia.objects.filter(usuaria=request.user, trimestre=trimestre,tipo=tipo).first()
    receta_hierro=False
    cita_extracciones=CitaExtracciones.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    if cita_extracciones.anemia:
        receta_hierro=True
    fecha_cita = cita_existente.fecha if cita_existente else None
    initial_data = {
        'fecha': fecha_cita,
        'receta_acido_folico': cita_existente.receta_acido_folico if cita_existente else None,
        'receta_hierro': cita_existente.receta_hierro if cita_existente else None,
        'observaciones':cita_existente.observaciones if cita_existente else None,
        'tipo':cita_existente.tipo if cita_existente else None,
        
    }
    form = CitaMedicinaFamiliaForm(initial=initial_data)
    return render(request, 'medicina_familia_hierro.html', {'form': form,'trimestre':trimestre,'receta_hierro':receta_hierro})


@login_required
def hierro(request):
    url = request.path
    trimestre = determinar_trimestre(url)
    print(trimestre)
    receta_hierro=False
    cita_extracciones=CitaExtracciones.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    if cita_extracciones.anemia:
        receta_hierro=True
    form = CitaMedicinaFamiliaForm(request.POST or None)
    tipo=determinar_tipo(url)
    cita_existente = CitaMedicinaFamilia.objects.filter(usuaria=request.user, trimestre=trimestre,tipo=tipo).first()
    if request.method == 'POST':
        form = CitaMedicinaFamiliaForm(request.POST or None)
        print('formulario valido',form.is_valid())
        if form.is_valid():
            return crear_actualizar_cita_medicina_familia_hierro(request,form)
        else:
            print(form.errors)
    else:
        return mostrar_formulario_hierro(request)
    return render(request, 'medicina_familia_hierro.html', {'form': form,'trimestre':trimestre,'receta_hierro':receta_hierro})


@login_required
def crear_actualizar_cita_medicina_familia_hierro(request,form):
    url = request.path
    trimestre = determinar_trimestre(url)
    tipo=determinar_tipo(url)
    cita_existente=CitaMedicinaFamilia.objects.filter(usuaria=request.user,trimestre=trimestre,tipo=tipo).first()
    receta_hierro=False
    cita_extracciones=CitaExtracciones.objects.filter(usuaria=request.user, trimestre=trimestre).first()
    if cita_extracciones.anemia:
        receta_hierro=True
    if cita_existente:
        print('0')
        cita_existente.fecha = form.cleaned_data['fecha']
        cita_existente.receta_acido_folico = form.cleaned_data['receta_acido_folico']
        cita_existente.receta_hierro = form.cleaned_data['receta_hierro']
        cita_existente.observaciones = form.cleaned_data['observaciones']
        cita_existente.save()
        
    else:   
        print('1') 
        nueva_cita = CitaMedicinaFamilia.objects.create(
            fecha=form.cleaned_data['fecha'],
            receta_acido_folico = form.cleaned_data['receta_acido_folico'],
            receta_hierro = form.cleaned_data['receta_hierro'],
            observaciones = form.cleaned_data['observaciones'],
            tipo = tipo,
            trimestre=trimestre,
            usuaria=request.user,
        )
        nueva_cita.save()
      
    
    return render(request, 'medicina_familia_hierro.html', {'form': form,'trimestre':trimestre,'receta_hierro':receta_hierro})

@login_required
def eliminar_cita_medicina_familia(request):
    url = request.path
    trimestre = determinar_trimestre(url)
    tipo=determinar_tipo(url)
    print(trimestre)
    form = CitaMedicinaFamiliaForm(request.POST or None)
    if request.method == 'POST':
        cita_existente = CitaMedicinaFamilia.objects.filter(usuaria=request.user, trimestre=trimestre,tipo=tipo).first()
        if cita_existente:
            cita_existente.delete()
        if trimestre==1:
            return redirect('/gestion_citas/citas_primer/')
        elif trimestre==2:
            return redirect('/gestion_citas/citas_segundo/')
        elif trimestre==3:
            return redirect('/gestion_citas/citas_tercer/')
        print('cita_existente',cita_existente)
    return render(request, 'eliminar_cita_medicina_familia.html',{'form':form,'trimestre':trimestre,'tipo':tipo})
    

@login_required
def acido_folico(request):
    url = request.path
    trimestre = determinar_trimestre(url)
    tipo=determinar_tipo(url)
    print(trimestre)
    form = CitaMedicinaFamiliaForm(request.POST or None)
    cita_existente = CitaMedicinaFamilia.objects.filter(usuaria=request.user, trimestre=trimestre,tipo=tipo).first()
    if request.method == 'POST':
        form = CitaMedicinaFamiliaForm(request.POST or None)
        print('formulario valido',form.is_valid())
        if form.is_valid():
            return crear_actualizar_cita_medicina_familia_acido_folico(request,form)
        else:
            print(form.errors)
    else:
        return mostrar_formulario_acido_folico(request)
    return render(request, 'medicina_familia_af.html', {'form': form,'trimestre':trimestre})

@login_required
def mostrar_formulario_acido_folico(request):
    url=request.path
    tipo=determinar_tipo(url)
    trimestre = determinar_trimestre(url)
    cita_existente = CitaMedicinaFamilia.objects.filter(usuaria=request.user, trimestre=trimestre,tipo=tipo).first()
   
    fecha_cita = cita_existente.fecha if cita_existente else None
    initial_data = {
        'fecha': fecha_cita,
        'receta_acido_folico': cita_existente.receta_acido_folico if cita_existente else None,
        'receta_hierro': cita_existente.receta_hierro if cita_existente else None,
        'observaciones':cita_existente.observaciones if cita_existente else None,
        'tipo':cita_existente.tipo if cita_existente else None,
        
    }
    form = CitaMedicinaFamiliaForm(initial=initial_data)
    return render(request, 'medicina_familia_af.html', {'form': form,'trimestre':trimestre})

@login_required
def crear_actualizar_cita_medicina_familia_acido_folico(request,form):
    url = request.path
    trimestre = determinar_trimestre(url)
    tipo=determinar_tipo(url)
    cita_existente=CitaMedicinaFamilia.objects.filter(usuaria=request.user,trimestre=trimestre,tipo=tipo).first()
   
    if cita_existente:
        print('0')
        cita_existente.fecha = form.cleaned_data['fecha']
        cita_existente.receta_acido_folico = form.cleaned_data['receta_acido_folico']
        cita_existente.receta_hierro = form.cleaned_data['receta_hierro']
        cita_existente.observaciones = form.cleaned_data['observaciones']
        cita_existente.save()
        
    else:   
        print('1') 
        nueva_cita = CitaMedicinaFamilia.objects.create(
            fecha=form.cleaned_data['fecha'],
            receta_acido_folico = form.cleaned_data['receta_acido_folico'],
            receta_hierro = form.cleaned_data['receta_hierro'],
            observaciones = form.cleaned_data['observaciones'],
            trimestre=trimestre,
            tipo=tipo,
            usuaria=request.user,
        )
        nueva_cita.save()
      
    
    return render(request, 'medicina_familia_af.html', {'form': form,'trimestre':trimestre})