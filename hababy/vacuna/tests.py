# Create your tests here.
import datetime
from django.test import TestCase
from vacuna.models import CitaVacuna
from django.contrib.auth.models import User
from django.utils import timezone
from vacuna.forms.forms import CitaVacunaForm

class VacunaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.cita = CitaVacuna.objects.create(
            usuaria=self.user,
            fecha=timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),
            nombre='tos_ferina',
            observaciones = 'observaciones'
        )

    def test_crear_cita(self):
        cita = CitaVacuna.objects.get(id=self.cita.id)
        expected_fecha = timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone())
        self.assertEqual(cita.fecha, expected_fecha)
        self.assertEqual(cita.usuaria, self.user)
        self.assertEqual(cita.nombre,self.cita.nombre)
        self.assertEqual(cita.observaciones, self.cita.observaciones)

    def test_actualizar_cita(self):
        cita = CitaVacuna.objects.get(id=self.cita.id)
        cita.fecha = timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone())
        cita.nombre = 'Nuevo nombre'
        cita.observaciones = 'Nuevas observaciones'
        cita.save()
        updated_cita = CitaVacuna.objects.get(id=self.cita.id)
        self.assertEqual(updated_cita.fecha, timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone()))
        self.assertEqual(updated_cita.nombre, 'Nuevo nombre')
        self.assertEqual(updated_cita.observaciones, 'Nuevas observaciones')

    def test_crear_cita_sin_fecha(self):
        form_data = {
            'usuaria': self.user.id,
            'nombre': 'Nombre vacuna',
            'observaciones': 'Ninguna'
        }
        form = CitaVacunaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('fecha' in form.errors)

    def test_eliminar_cita(self):
        cita = CitaVacuna.objects.get(id=self.cita.id)
        cita.delete()
        with self.assertRaises(CitaVacuna.DoesNotExist):
            CitaVacuna.objects.get(id=self.cita.id)