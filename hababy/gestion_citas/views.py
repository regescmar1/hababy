from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from extracciones.models import CitaExtracciones

@login_required
def gestion_citas(request):
    return render(request,'gestion_citas.html')

@login_required
def citas_primer(request):
    receta_hierro=False
    anemia= CitaExtracciones.objects.filter(usuaria=request.user, trimestre=1,anemia=True)
    if anemia:
        receta_hierro=True
    return render(request,'citas_primer.html',{'receta_hierro':receta_hierro})

@login_required
def citas_segundo(request):
    receta_hierro=False
    anemia= CitaExtracciones.objects.filter(usuaria=request.user, trimestre=2,anemia=True)
    if anemia:
        receta_hierro=True
    return render(request,'citas_segundo.html',{'receta_hierro':receta_hierro})

@login_required
def citas_tercer(request):
    receta_hierro=False
    anemia= CitaExtracciones.objects.filter(usuaria=request.user, trimestre=3,anemia=True)
    if anemia:
        receta_hierro=True
    return render(request,'citas_tercer.html',{'receta_hierro':receta_hierro})
    
