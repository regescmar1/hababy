# Create your tests here.
import datetime
from django.test import TestCase
from odontologia.models import CitaOdontologia
from django.contrib.auth.models import User
from django.utils import timezone

from odontologia.forms.forms import CitaOdontologiaForm

class OdontologiaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.cita = CitaOdontologia.objects.create(
            usuaria=self.user,
            fecha=timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),
            limpieza=True,
            observaciones="abc",
        )

    def test_crear_cita(self):
        cita = CitaOdontologia.objects.get(id=self.cita.id)
        expected_fecha = timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone())
        self.assertEqual(cita.fecha, expected_fecha)
        self.assertEqual(cita.usuaria, self.user)
        self.assertTrue(cita.limpieza)
        self.assertEqual(cita.observaciones, self.cita.observaciones)

    def test_actualizar_cita(self):
        cita = CitaOdontologia.objects.get(id=self.cita.id)
        cita.fecha = timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone())
        cita.limpieza = False
        cita.observaciones = 'Nuevas observaciones'
        cita.save()
        updated_cita = CitaOdontologia.objects.get(id=self.cita.id)
        self.assertEqual(updated_cita.fecha, timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone()))
        self.assertFalse(updated_cita.limpieza)
        self.assertEqual(updated_cita.observaciones, 'Nuevas observaciones')

    def test_crear_cita_sin_fecha(self):
        form_data = {
            'usuaria': self.user.id,
            'limpieza': False,
            'observaciones': 'Ninguna'
        }
        form = CitaOdontologiaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('fecha' in form.errors)

    def test_eliminar_cita(self):
        cita = CitaOdontologia.objects.get(id=self.cita.id)
        cita.delete()
        with self.assertRaises(CitaOdontologia.DoesNotExist):
            CitaOdontologia.objects.get(id=self.cita.id)