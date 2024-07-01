from educacion_maternal.forms.forms import SesionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from educacion_maternal.models import Sesion

# Create your views here.
@login_required
def educacion_maternal(request):
    sesiones_existentes=Sesion.objects.filter(usuaria=request.user).order_by('fecha')
    return render(request, 'educacion_maternal.html',{'sesiones_existentes':sesiones_existentes})

@login_required
def sesion(request, sesion_id=None):
    if request.method == 'POST':
        form = SesionForm(request.POST)
        if form.is_valid():
            if sesion_id:
                return actualizar_sesion(request, form, sesion_id)
            else:
                return crear_sesion(request, form)
        else:
            print(form.errors)
    else:
        return mostrar_formulario(request, sesion_id)

@login_required
def crear_sesion(request):
    print('entraqui')
    if request.method == 'POST':
        form = SesionForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            nueva_sesion=Sesion(
                fecha=form.cleaned_data['fecha'],
                titulo=form.cleaned_data['titulo'],
                observaciones=form.cleaned_data['observaciones'],
                usuaria=request.user
            )
            print(nueva_sesion.titulo)
            nueva_sesion.save()
            return redirect('sesion', sesion_id=nueva_sesion.id)
    else:
        print('1')
        form = SesionForm()
    return render(request, 'crear_sesion.html', {'form': form})

@login_required
def actualizar_sesion(request, form, sesion_id):
    sesion_existente = get_object_or_404(Sesion, id=sesion_id)
    if form.is_valid():
        sesion_existente.fecha = form.cleaned_data['fecha']
        sesion_existente.titulo = form.cleaned_data['titulo']
        sesion_existente.observaciones = form.cleaned_data['observaciones']
        sesion_existente.save()
        return render(request, 'sesion.html', {'form': form,'sesion_id':sesion_id,'sesion_existente':sesion_existente})


@login_required
def mostrar_formulario(request, sesion_id):
    sesion_existente = get_object_or_404(Sesion, id=sesion_id)
    fecha_sesion = sesion_existente.fecha if sesion_existente else None
    initial_data = {
        'fecha': fecha_sesion,
        'titulo': sesion_existente.titulo if sesion_existente else None,
        'observaciones': sesion_existente.observaciones if sesion_existente else None,
    }
    form = SesionForm(initial=initial_data)
    return render(request, 'sesion.html', {'form': form, 'sesion_existente': sesion_existente, 'sesion_id': sesion_id})

@login_required
def eliminar_sesion(request,sesion_id):
    
    form = SesionForm(request.POST or None)
    if request.method == 'POST':
        sesion_existente = get_object_or_404(Sesion, id=sesion_id)
        if sesion_existente:
            sesion_existente.delete()

            return redirect('/educacion_maternal/')
    return render(request, 'eliminar_sesion.html',{'form':form})