from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from obstetra.forms.forms import CitaObstetraForm

from obstetra.models import CitaObstetra

# Create your views here.

def determinar_trimestre_y_orden(url):
    trimestre = None
    orden = None
    if 'citas_primer' in url:
        trimestre = 1
        orden=1
    elif 'citas_segundo' in url:
        trimestre = 2
        orden=1
    elif 'citas_tercer' in url:
        trimestre = 3
    
    if 'uno' in url:
        orden = 1
    elif 'dos' in url:
        orden = 2
    elif 'tres' in url:
        orden = 3

    return trimestre, orden


@login_required
def mostrar_formulario(request):
    url=request.path
    trimestre, orden = determinar_trimestre_y_orden(url)
    cita_existente = CitaObstetra.objects.filter(usuaria=request.user, trimestre=trimestre, orden=orden).first()
    fecha_cita = cita_existente.fecha if cita_existente else None
    initial_data = {
        'fecha': fecha_cita,
        'peso': cita_existente.peso if cita_existente else None,
        'altura': cita_existente.altura if cita_existente else None,
        'tas': cita_existente.tas if cita_existente else None,
        'tad': cita_existente.tad if cita_existente else None,
        'imc':cita_existente.imc if cita_existente else None,
        'observaciones':cita_existente.observaciones if cita_existente else None,
        'monitores':cita_existente.monitores if cita_existente else None,
    }
    form = CitaObstetraForm(initial=initial_data)
    return render(request, 'obstetra.html', {'form': form,'trimestre':trimestre,'orden':orden})

@login_required
def obstetra(request):
    url = request.path
    trimestre, orden = determinar_trimestre_y_orden(url)
    print(trimestre)
    print(orden)
    form = CitaObstetraForm(request.POST or None)
    cita_existente = CitaObstetra.objects.filter(usuaria=request.user, trimestre=trimestre, orden=orden).first()
    if request.method == 'POST':
        form = CitaObstetraForm(request.POST or None)
        print('formulario valido',form.is_valid())
        if form.is_valid():
            return crear_actualizar_cita_obstetra(request,form)
        else:
            print(form.errors)
    else:
        return mostrar_formulario(request)
    return render(request, 'obstetra.html', {'form': form,'trimestre':trimestre,'orden':orden})


@login_required
def crear_actualizar_cita_obstetra(request,form):
    url = request.path
    trimestre, orden = determinar_trimestre_y_orden(url)
    cita_existente=CitaObstetra.objects.filter(usuaria=request.user,trimestre=trimestre,orden=orden).first()
    if cita_existente:
        print('0')
        cita_existente.fecha = form.cleaned_data['fecha']
        cita_existente.peso = form.cleaned_data['peso']
        cita_existente.altura = form.cleaned_data['altura']
        if cita_existente.peso and cita_existente.altura:
            cita_existente.imc = cita_existente.peso / (cita_existente.altura ** 2)
        cita_existente.tas = form.cleaned_data['tas']
        cita_existente.tad = form.cleaned_data['tad']
        cita_existente.observaciones = form.cleaned_data['observaciones']
        cita_existente.monitores = form.cleaned_data['monitores']
        cita_existente.save()
        
    else:   
        print('1') 
        nueva_cita = CitaObstetra.objects.create(
            fecha=form.cleaned_data['fecha'],
            peso=form.cleaned_data['peso'],
            altura=form.cleaned_data['altura'],
            tas=form.cleaned_data['tas'],
            tad=form.cleaned_data['tad'],
            observaciones=form.cleaned_data['observaciones'],
            trimestre=trimestre,
            orden=orden,
            monitores=form.cleaned_data['monitores'],
            usuaria=request.user
        )

        if nueva_cita.peso is not None and nueva_cita.peso != 0 and nueva_cita.altura is not None and nueva_cita.altura != 0:
            print("Peso:", nueva_cita.peso)
            print("Altura:", nueva_cita.altura)
            if nueva_cita.peso and nueva_cita.altura:
                nueva_cita.imc = nueva_cita.peso / (nueva_cita.altura ** 2)
            nueva_cita.save()
        else:
            print("Peso o altura no válidos:", nueva_cita.peso, nueva_cita.altura)
        
    
    return render(request, 'obstetra.html', {'form': form,'trimestre':trimestre,'orden':orden})



@login_required
def eliminar_cita_obstetra(request):
    url = request.path
    trimestre, orden = determinar_trimestre_y_orden(url)
    print(trimestre)
    print(orden)
    form = CitaObstetraForm(request.POST or None)
    if request.method == 'POST':
        cita_existente = CitaObstetra.objects.filter(usuaria=request.user, trimestre=trimestre, orden=orden).first()
        if cita_existente:
            cita_existente.delete()
        if trimestre==1:
            return redirect('/gestion_citas/citas_primer/')
        elif trimestre==2:
            return redirect('/gestion_citas/citas_segundo/')
        elif trimestre==3:
            return redirect('/gestion_citas/citas_tercer/')
    return render(request, 'eliminar_cita_obstetra.html',{'form':form,'trimestre':trimestre,'orden':orden})
    