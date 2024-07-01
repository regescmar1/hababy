# Create your views here.
from django.shortcuts import render,redirect 
from odontologia.models import CitaOdontologia
from django.contrib.auth.decorators import login_required
from odontologia.forms.forms import CitaOdontologiaForm


@login_required
def mostrar_formulario(request):
    cita_existente = CitaOdontologia.objects.filter(usuaria=request.user).first()
    fecha_cita = cita_existente.fecha if cita_existente else None
    initial_data = {
        'eliminar_cita_odontologia_id':cita_existente.id if cita_existente else None,
        'fecha': fecha_cita,
        'limpieza': cita_existente.limpieza if cita_existente else None,
        'observaciones': cita_existente.observaciones if cita_existente else None
    }
    form = CitaOdontologiaForm(initial=initial_data)
    return render(request, 'odontologia.html', {'form': form,'cita_existente':cita_existente})

@login_required
def odontologia(request):
    if request.method == 'POST':
        form = CitaOdontologiaForm(request.POST or None)
        print('formulario valido',form.is_valid())
        if form.is_valid():
            return crear_actualizar_cita_odontologia(request,form)
        else:
            print(form.errors)
    else:
        return mostrar_formulario(request)
    return render(request, 'odontologia.html', {'form': form})

@login_required
def eliminar_cita_odontologia(request):
    if request.method == 'POST':
        cita_existente=CitaOdontologia.objects.filter(usuaria=request.user).first()
        if cita_existente:
            cita_existente.delete()
        return redirect('/gestion_citas/citas_primer/')
    return render(request,'eliminar_cita_odontologia.html')

@login_required
def crear_actualizar_cita_odontologia(request,form):
    cita_existente=CitaOdontologia.objects.filter(usuaria=request.user).first()
    if cita_existente:
        cita_existente.fecha = form.cleaned_data['fecha']
        cita_existente.limpieza = form.cleaned_data['limpieza']
        cita_existente.observaciones = form.cleaned_data['observaciones']
        cita_existente.save()
        return redirect('odontologia')
    else:
        nueva_cita = CitaOdontologia.objects.create(
            fecha=form.cleaned_data['fecha'],
            limpieza = form.cleaned_data['limpieza'],
            observaciones = form.cleaned_data['observaciones'],
            usuaria=request.user
        )
        nueva_cita.save()
        return redirect('odontologia')