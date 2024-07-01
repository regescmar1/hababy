# Create your tests here.
from django.test import Client
from .views import enviar_correo_confirmacion
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from autenticacion.forms.forms import OlvidoContraseniaForm, RegistroForm

class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword',email='testuser@testuser.com')

    def test_login_usuaria_correcto(self):
        client = Client()
        response = client.post(reverse('login_usuaria'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)

    def test_login_incorrecto_redireccionamiento(self):
        response = self.client.post(reverse('login_usuaria'), {'username': 'testuser', 'password': 'paaaasss'})
        self.assertRedirects(response, reverse('login_incorrecto'))

    def test_login_completado(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('login_completado'))
        self.assertEqual(response.status_code, 302)

    def test_logout_usuaria(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout_usuaria'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('principal'))

class OlvidoContraseniaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword',email='testuser@testuser.com')

    def test_olvido_contrasenia_get(self):
        response = self.client.get(reverse('olvido_contrasenia'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], OlvidoContraseniaForm)

    def test_olvido_contrasenia_post(self):
        response = self.client.post(reverse('olvido_contrasenia'), {'email': 'testuser@testuser.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verificar_codigo_para_contrasenia'))
        self.assertIn('codigo_confirmacion', self.client.session)
        self.assertIn('registro_data', self.client.session)
        self.assertIn('email_olvido', self.client.session)
        self.assertEqual(self.client.session['email_olvido'], 'testuser@testuser.com')

class VerificarCodigoParaCorreoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.session['codigo_confirmacion'] = '123456'

    def test_verificar_codigo_para_correo_get(self):
        response = self.client.get(reverse('verificar_codigo_para_correo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'verificar_codigo.html')

    def test_verificar_codigo_para_correo_incorrecto(self):
        response = self.client.post(reverse('verificar_codigo_para_correo'), {'codigo_confirmacion': '654321'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'codigo_error.html')

class VerificarCodigoParaContraseniaTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.session['codigo_confirmacion'] = '123456'

    def test_verificar_codigo_incorrecto(self):
        response = self.client.post(reverse('verificar_codigo_para_contrasenia'), {'codigo_confirmacion': '654321'})
        self.assertTemplateUsed(response, 'codigo_error.html')

    def test_get_request(self):
        response = self.client.get(reverse('verificar_codigo_para_contrasenia'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'verificar_codigo.html')

class EnviarCorreoConfirmacionTestCase(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_enviar_correo_confirmacion(self):
        destinatario = 'testuser@example.com'
        codigo = '123456'
        enviar_correo_confirmacion(destinatario, codigo)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Código de confirmación de registro')
        self.assertEqual(mail.outbox[0].body, f'Su código de confirmación es: {codigo}')
        self.assertEqual(mail.outbox[0].to, [destinatario])

class RegistroTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registro_post(self):
        response = self.client.post(reverse('registro'), {
            'username': 'testuser2',
            'email': 'testuser2@test.com',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('codigo_confirmacion', self.client.session)
        self.assertIn('registro_data', self.client.session)

    def test_registro_get(self):
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro.html')
        self.assertIsInstance(response.context['form'], RegistroForm)

class MiPerfilTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@test.com')

    def test_mi_perfil_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('mi_perfil'), {
            'username': 'newusername',
            'email': 'newemail@test.com',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@test.com')
        self.assertTrue(self.user.check_password('newpassword'))
        self.assertRedirects(response, reverse('perfil_actualizado'))

    def test_mi_perfil_actualizado(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('perfil_actualizado'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'perfil_actualizado.html')

    def test_eliminar_mi_perfil(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('eliminar_mi_perfil'))
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertRedirects(response, '/')