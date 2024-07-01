from django.test import Client,TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from educacion_maternal.forms.forms import SesionForm
from educacion_maternal.models import Sesion
from django.urls import reverse
# Create your tests here.
class SesionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.sesion = Sesion.objects.create(
            usuaria=self.user,
            fecha=timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),
            titulo='sesion',
            observaciones = 'observaciones'
        )

    def test_educacion_maternal_sesiones(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('educacion_maternal'))
        self.assertEqual(response.status_code, 302)

    def test_crear_sesion(self):
        sesion = Sesion.objects.get(id=self.sesion.id)
        expected_fecha = timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone())
        self.assertEqual(sesion.fecha, expected_fecha)
        self.assertEqual(sesion.usuaria, self.user)
        self.assertEqual(sesion.titulo,self.sesion.titulo)
        self.assertEqual(sesion.observaciones, self.sesion.observaciones)

    def test_actualizar_sesion(self):
        sesion = Sesion.objects.get(id=self.sesion.id)
        sesion.fecha = timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone())
        sesion.titulo = 'Nuevo titulo'
        sesion.observaciones = 'Nuevas observaciones'
        sesion.save()
        updated_sesion= Sesion.objects.get(id=self.sesion.id)
        self.assertEqual(updated_sesion.fecha, timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone()))
        self.assertEqual(updated_sesion.titulo, 'Nuevo titulo')
        self.assertEqual(updated_sesion.observaciones, 'Nuevas observaciones')

    def test_crear_sesion_sin_fecha(self):
        form_data = {
            'usuaria': self.user.id,
            'titulo': 'Titulo sesion',
            'observaciones': 'Ninguna'
        }
        form = SesionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('fecha' in form.errors)

    def test_crear_sesion_sin_titulo(self):
        form_data = {
            'usuaria': self.user.id,
            'fecha': timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),
            'observaciones': 'Ninguna'
        }
        form = SesionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('titulo' in form.errors)

    def test_eliminar_sesion(self):
        sesion = Sesion.objects.get(id=self.sesion.id)
        sesion.delete()
        with self.assertRaises(Sesion.DoesNotExist):
            Sesion.objects.get(id=self.sesion.id)