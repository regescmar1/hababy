# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from autenticacion.forms.forms import    ModificarContraseniaForm, OlvidoContraseniaForm,UsuariaLoginForm,RegistroForm,MiPerfilForm
import braintree
from django.core.exceptions import ObjectDoesNotExist
import random
import json
import logging
from autenticacion.models import EstadoPago
logging.basicConfig(level=logging.DEBUG)

def login_incorrecto(request):
    return render(request, 'login_incorrecto.html')

def login_usuaria(request):
    if request.method == 'POST':
        form = UsuariaLoginForm(request.POST)
        print("Datos del formulario recibidos:", request.POST)
        if form.is_valid():
            print("El formulario es válido")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print(username)
            print(password)
            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    return redirect ('/administrador/')
                else:
                    return redirect('/autenticacion/login_completado/')
            else:
                print("Autenticación fallida: Usuario o contraseña incorrectos")
                return redirect('/autenticacion/login_incorrecto/')
        else:
            print("El formulario no es válido")
            return redirect('/autenticacion/login_incorrecto/')
    else:
        form = UsuariaLoginForm()
    return render(request, 'login_usuaria.html', {'form': form})

@login_required
def login_completado(request):
    try:
        estado_pago = EstadoPago.objects.get(usuario=request.user)
        if estado_pago.pago_completado:
            return render(request, 'login_completado.html')
        else:
            return redirect('/autenticacion/registro/braintree_social')
    except ObjectDoesNotExist:
        return redirect('/autenticacion/registro/braintree_social')

@login_required
def logout_usuaria(request):
    logout(request)
    return redirect(reverse('principal'))

def enviar_correo_confirmacion(destinatario, codigo):
    asunto = 'Código de confirmación de registro'
    mensaje = f'Su código de confirmación es: {codigo}'
    try:
        send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [destinatario])
    except Exception as e:
        print('Error al enviar el correo:', e)

def verificar_codigo_para_correo(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo_confirmacion')
        codigo_correcto = request.session.get('codigo_confirmacion')
        if codigo_ingresado == codigo_correcto:
            return redirect('braintree')
        else:
            return render(request, 'codigo_error.html')
    return render(request, 'verificar_codigo.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            codigo_confirmacion = ''.join(random.choices('0123456789', k=6))
            request.session['codigo_confirmacion'] = codigo_confirmacion
            enviar_correo_confirmacion(form.cleaned_data['email'], codigo_confirmacion)
            request.session['registro_data']= form.cleaned_data
            return redirect('verificar_codigo_para_correo')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def braintree_view(request):
    print('000')
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce')
        print('0:',nonce)
        if nonce:
            gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    environment=braintree.Environment.Sandbox,
                    merchant_id=settings.BRAINTREE_MERCHANT_ID,
                    public_key=settings.BRAINTREE_PUBLIC_KEY,
                    private_key=settings.BRAINTREE_PRIVATE_KEY
                )
            )
            result = gateway.transaction.sale({
                "amount": "1.99",  
                "payment_method_nonce": nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })
            print(result.is_success)
            if result.is_success:
                registro_data = request.session.get('registro_data')
                print("2Datos del formulario almacenados en la sesión:", registro_data)
                if registro_data:
                    username = registro_data['username']
                    email = registro_data['email']
                    password = registro_data['password']
                    user = User.objects.create_user(username=username, email=email, password=password)
                    print("3Usuario creado:", user)
                    del request.session['registro_data']
                    return redirect('registro_completado')
    else:
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=braintree.Environment.Sandbox,
                merchant_id=settings.BRAINTREE_MERCHANT_ID,
                public_key=settings.BRAINTREE_PUBLIC_KEY,
                private_key=settings.BRAINTREE_PRIVATE_KEY
            )
        )
        client_token = gateway.client_token.generate()
        return render(request, 'braintree.html', {'braintree_client_token': client_token})

def procesar_pago(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        nonce = body_data.get('nonce')
        if nonce:
            gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    environment=braintree.Environment.Sandbox,
                    merchant_id=settings.BRAINTREE_MERCHANT_ID,
                    public_key=settings.BRAINTREE_PUBLIC_KEY,
                    private_key=settings.BRAINTREE_PRIVATE_KEY
                )
            )
            result = gateway.transaction.sale({
                "amount": "1.99",  
                "payment_method_nonce": nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })
            if result.is_success:
                registro_data = request.session.get('registro_data')
                if registro_data:
                    username = registro_data['username']
                    email = registro_data['email']
                    password = registro_data['password']
                    user = User.objects.create_user(username=username, email=email, password=password)
                    estado_pago = EstadoPago(usuario=user, pago_completado=True)
                    estado_pago.save()
                    del request.session['registro_data']
                    return JsonResponse({"status": "success"})
                else:
                    return JsonResponse({"status": "error", "message": "Datos de registro no encontrados en la sesión"})
            else:
                error_message = result.message
                return JsonResponse({"status": "error", "message": error_message})
        else:
            return JsonResponse({"status": "error", "message": "Nonce de pago no proporcionado"})
    else:
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

def registro_completado(request):
    return render(request, 'registro_completado.html')

def olvido_contrasenia(request):
    if request.method == 'POST':
        form = OlvidoContraseniaForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            codigo_confirmacion = ''.join(random.choices('0123456789', k=6))
            request.session['codigo_confirmacion'] = codigo_confirmacion
            enviar_correo_confirmacion(form.cleaned_data['email'], codigo_confirmacion)
            request.session['registro_data']= form.cleaned_data
            request.session['email_olvido']=form.cleaned_data['email']
            return redirect('verificar_codigo_para_contrasenia')
    else:
        form = OlvidoContraseniaForm()
    return render(request, 'olvido_contrasenia.html', {'form': form})

def verificar_codigo_para_contrasenia(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo_confirmacion')
        codigo_correcto = request.session.get('codigo_confirmacion')
        if codigo_ingresado == codigo_correcto:
            return redirect('modificar_contrasenia')
        else:
            return render(request, 'codigo_error.html')
    return render(request, 'verificar_codigo.html')

def modificar_contrasenia(request):
    email_olvido= request.session.get('email_olvido')
    print('email_olvido',email_olvido)
    user = get_object_or_404(User, email=email_olvido)
    if request.method == 'POST':
        form = ModificarContraseniaForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            print('nueva contraseña1: ',new_password1)
            new_password2 = form.cleaned_data['new_password2']
            print('nueva contraseña2:',new_password2)
            if new_password1 and new_password2 and new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                print('usuario',user)
                update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada exitosamente.')
            return redirect('/autenticacion/login_usuaria/')
    else:
        form = ModificarContraseniaForm()
    return render(request, 'modificar_contrasenia.html',{'form': form})

def braintree_social(request):
    print('000')
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce')
        print('0:',nonce)
        if nonce:
            gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    environment=braintree.Environment.Sandbox,
                    merchant_id=settings.BRAINTREE_MERCHANT_ID,
                    public_key=settings.BRAINTREE_PUBLIC_KEY,
                    private_key=settings.BRAINTREE_PRIVATE_KEY
                )
            )
            result = gateway.transaction.sale({
                "amount": "1.99",  
                "payment_method_nonce": nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })
            print(result.is_success)
            if result.is_success:
                ultimo_usuario = User.objects.latest('id')
                print(ultimo_usuario)
                estado_pago=EstadoPago(usuaria=ultimo_usuario,pago_completado=True)
                estado_pago.save()
                return render(request,'registro_completado.html',{'estado_pago':estado_pago})  
    else:
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=braintree.Environment.Sandbox,
                merchant_id=settings.BRAINTREE_MERCHANT_ID,
                public_key=settings.BRAINTREE_PUBLIC_KEY,
                private_key=settings.BRAINTREE_PRIVATE_KEY
            )
        )
        client_token = gateway.client_token.generate()
        return render(request, 'braintree_social.html', {'braintree_client_token': client_token})

def procesar_pago_social(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        nonce = body_data.get('nonce')
        if nonce:
            gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    environment=braintree.Environment.Sandbox,
                    merchant_id=settings.BRAINTREE_MERCHANT_ID,
                    public_key=settings.BRAINTREE_PUBLIC_KEY,
                    private_key=settings.BRAINTREE_PRIVATE_KEY
                )
            )
            result = gateway.transaction.sale({
                "amount": "1.99",  
                "payment_method_nonce": nonce,
                "options": {
                    "submit_for_settlement": True
                }
            })
            if result.is_success:
                ultimo_usuario = User.objects.latest('id')
                estado_pago=EstadoPago(usuario=ultimo_usuario,pago_completado=True)
                estado_pago.save()
                return JsonResponse({"status": "success"})
            else:
                error_message = result.message
                return JsonResponse({"status": "error", "message": error_message})
        else:
            return JsonResponse({"status": "error", "message": "Nonce de pago no proporcionado"})
    else:
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

@login_required
def mi_perfil(request):
    user=request.user
    if request.method == 'POST':
        form = MiPerfilForm(request.POST, initial={'usuario_id': user.id})
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1 and new_password2 and new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('perfil_actualizado')
    else:
        form = MiPerfilForm(initial={'username': user.username, 'email': user.email,'usuario_id': user.id})
    return render(request, 'mi_perfil.html', {'form': form})

@login_required
def perfil_actualizado(request):
    return render(request, 'perfil_actualizado.html')

@login_required
def eliminar_mi_perfil(request):
    form=MiPerfilForm(request.POST or None)
    if request.method== 'POST':
        perfil_a_eliminar=User.objects.filter(username=request.user.username).first()
        if perfil_a_eliminar:
            perfil_a_eliminar.delete()
            return redirect('/')
    else:
        return render(request, 'eliminar_mi_perfil.html',{'form':form})