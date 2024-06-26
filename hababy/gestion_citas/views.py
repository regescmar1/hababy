from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required
def gestion_citas(request):
    return render(request,'gestion_citas.html')

@login_required
def citas_primer(request):
    return render(request,'citas_primer.html')

@login_required
def citas_segundo(request):
    return render(request,'citas_segundo.html')

@login_required
def citas_tercer(request):
   
    return render(request,'citas_tercer.html')
    
