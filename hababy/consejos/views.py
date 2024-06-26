from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def consejos(request):

    return render(request,'consejos.html')

@login_required
def nauseas(request):
    return render(request,'nauseas.html')

@login_required
def ejercicios(request):
    return render(request,'ejercicios.html')

@login_required
def nutricion(request):
    return render(request,'nutricion.html')

@login_required
def lactancia(request):
    return render(request,'lactancia.html')

@login_required
def bolso_hospital(request):
    return render(request,'bolso_hospital.html')

@login_required
def contracciones(request):
    return render(request,'contracciones.html')

@login_required
def induccion_al_parto(request):
    return render(request,'induccion_al_parto.html')

@login_required
def cordon_umbilical(request):
    return render(request,'cordon_umbilical.html')

@login_required
def suelo_pelvico(request):
    return render(request,'suelo_pelvico.html')


