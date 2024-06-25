from django.shortcuts import render


# Create your views here.
def principal(request):
    return render(request,'principal.html')

def acerca_de(request):
    return render(request,'acerca_de.html')

def contacto(request):
    return render(request,'contacto.html')


def politica_privacidad(request):
    return render(request,'politica_privacidad.html')




