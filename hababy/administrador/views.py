from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages

from administrador.forms.forms import PerfilUsuariaForm
from extracciones.models import CitaExtracciones, CurvaLarga
from matrona.models import CitaMatrona
from medicina_familia.models import CitaMedicinaFamilia
from obstetra.models import CitaObstetra
from odontologia.models import CitaOdontologia
from vacuna.models import CitaVacuna



# Create your views here.
@login_required
def administrador(request):
    return render(request, 'administrador.html')

@login_required
def gestion_usuarias(request):
    usuarias=User.objects.filter().order_by('id')
    return render(request, 'gestion_usuarias.html',{'usuarias':usuarias})


@login_required
def usuaria(request,usuaria_id=None):
    usuaria = get_object_or_404(User, id=usuaria_id)
    if request.method == 'POST':
        form = PerfilUsuariaForm(request.POST, initial={'usuario_id': usuaria.id})
        if form.is_valid():
            usuaria.username = form.cleaned_data['username']
            usuaria.email = form.cleaned_data['email']
            usuaria.save()
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1 and new_password2 and new_password1 == new_password2:
                usuaria.set_password(new_password1)
                usuaria.save()
                update_session_auth_hash(request, usuaria)
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('perfil_actualizado_admin')
    else:
        form = PerfilUsuariaForm(initial={'username': usuaria.username, 'email': usuaria.email,'usuario_id': usuaria.id}) 
    
    return render(request, 'usuaria.html', {'form': form,'usuaria_id':usuaria_id})

@login_required
def crear_usuaria(request):
    if request.method == 'POST':
        form = PerfilUsuariaForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('/administrador/gestion_usuarias/')
    else:
        form = PerfilUsuariaForm()
    return render(request, 'usuaria.html', {'form': form})


@login_required
def perfil_actualizado_admin(request):
    return render(request, 'perfil_actualizado_admin.html')


@login_required
def eliminar_usuaria(request,usuaria_id):
    perfil_a_eliminar=get_object_or_404(User, id=usuaria_id)
    if request.method== 'POST':
        perfil_a_eliminar.delete()
        return redirect('/administrador/gestion_usuarias/')
    else:
        form = PerfilUsuariaForm()
        return render(request, 'eliminar_usuaria.html', {'form': form})
    
@login_required
def citas(request):
    citas_curva_larga =CurvaLarga.objects.count()
    citas_extracciones = CitaExtracciones.objects.count()
    citas_matrona = CitaMatrona.objects.count()
    citas_medicina_familia = CitaMedicinaFamilia.objects.count()
    citas_obstetra = CitaObstetra.objects.count()
    citas_odontologia = CitaOdontologia.objects.count()
    citas_vacuna = CitaVacuna.objects.count()

    usuarias_dict=citas_por_usuaria(request)
    media=media_citas(request)
    max=max_num_citas(request)
    min=min_num_citas(request)
    

    return render(request, 'citas.html',{'min':min,'max':max,'media':media,'usuarias_dict': usuarias_dict,
                                         'citas_curva_larga': citas_curva_larga,'citas_extracciones':citas_extracciones,
                                         'citas_matrona':citas_matrona,'citas_medicina_familia':citas_medicina_familia,
                                         'citas_obstetra':citas_obstetra,'citas_odontologia':citas_odontologia,'citas_vacuna':citas_vacuna})

@login_required
def citas_por_usuaria(request):
    usuarias=User.objects.all()
    usuarias_dict = {}
    for usuaria in usuarias:
        citas_curva_larga =CurvaLarga.objects.filter(usuaria=usuaria).count()
        citas_extracciones = CitaExtracciones.objects.filter(usuaria=usuaria).count()
        citas_matrona = CitaMatrona.objects.filter(usuaria=usuaria).count()
        citas_medicina_familia = CitaMedicinaFamilia.objects.filter(usuaria=usuaria).count()
        citas_obstetra = CitaObstetra.objects.filter(usuaria=usuaria).count()
        citas_odontologia = CitaOdontologia.objects.filter(usuaria=usuaria).count()
        citas_vacuna = CitaVacuna.objects.filter(usuaria=usuaria).count()
        total=citas_curva_larga+citas_extracciones+citas_matrona+citas_medicina_familia+citas_obstetra+citas_odontologia+citas_vacuna
        usuarias_dict[usuaria] = total
    return usuarias_dict

@login_required
def media_citas(request):
    usuarias_dict=citas_por_usuaria(request)
    num_usuarias=User.objects.all().count()
    suma=sum(usuarias_dict.values())
    media=suma/num_usuarias
    return media

@login_required
def max_num_citas(request):
    usuarias_dict = citas_por_usuaria(request)
    max_citas = 0
    for total_citas in usuarias_dict.values():
        if total_citas > max_citas:
            max_citas = total_citas
    return max_citas

@login_required
def min_num_citas(request):
    usuarias_dict = citas_por_usuaria(request)
    min_citas = float('inf')
    for total_citas in usuarias_dict.values():
        if total_citas < min_citas:
            min_citas = total_citas
    return min_citas

@login_required
def gestion_extracciones(request):
    o_sullivan_larga_positivo =CurvaLarga.objects.filter(analisis_normal=False).count()
    o_sullivan_normal_positivo=CitaExtracciones.objects.filter(test_o_sullivan_positivo=True).count()
    anemia=CitaExtracciones.objects.filter(anemia=True).count()
    analisis_normal=CitaExtracciones.objects.filter(analisis_normal=True).count()
    rh_negativo=CitaExtracciones.objects.filter(rh_negativo=True).count()
  
    return render(request, 'gestion_extracciones.html',{'o_sullivan_larga_positivo':o_sullivan_larga_positivo,
                                                        'o_sullivan_normal_positivo':o_sullivan_normal_positivo,
                                                        'anemia':anemia,'analisis_normal': analisis_normal,
                                                        'rh_negativo':rh_negativo})


@login_required
def gestion_vacunas(request):
    gripe=CitaVacuna.objects.filter(nombre='gripe').count()
    antid=CitaVacuna.objects.filter(nombre='antid').count()
    tos_ferina=CitaVacuna.objects.filter(nombre='tos_ferina').count()
  
    return render(request, 'gestion_vacunas.html',{'gripe':gripe,'antid':antid,'tos_ferina':tos_ferina})

@login_required
def gestion_odontologia(request):
    num_usuarias=User.objects.all().count()
    limpieza_si=CitaOdontologia.objects.filter(limpieza=True).count()
    limpieza_no=num_usuarias-limpieza_si
    print('limpieza si',limpieza_si)
    return render(request, 'gestion_odontologia.html',{'limpieza_si':limpieza_si,'limpieza_no':limpieza_no})