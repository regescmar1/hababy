# Create your tests here.
import datetime
from django.test import TestCase
from medicina_familia.models import CitaMedicinaFamilia
from django.contrib.auth.models import User
from django.utils import timezone
from medicina_familia.forms.forms import CitaMedicinaFamiliaForm

class MedicinaFamiliaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.cita = CitaMedicinaFamilia.objects.create(
            usuaria=self.user,
            fecha=timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),
            receta_acido_folico=True,
            observaciones="abc",
            trimestre=1
        )

    def test_crear_cita(self):
        cita = CitaMedicinaFamilia.objects.get(id=self.cita.id)
        expected_fecha = timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone())
        self.assertEqual(cita.fecha, expected_fecha)
        self.assertEqual(cita.usuaria, self.user)
        self.assertTrue(cita.receta_acido_folico)
        self.assertEqual(cita.observaciones, self.cita.observaciones)
        self.assertEqual(cita.trimestre, self.cita.trimestre)

    def test_actualizar_cita(self):
        cita = CitaMedicinaFamilia.objects.get(id=self.cita.id)
        cita.fecha = timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone())
        cita.receta_acido_folico = False
        cita.observaciones = 'Nuevas observaciones'
        cita.save()
        updated_cita = CitaMedicinaFamilia.objects.get(id=self.cita.id)
        self.assertEqual(updated_cita.fecha, timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone()))
        self.assertFalse(updated_cita.receta_acido_folico)
        self.assertEqual(updated_cita.observaciones, 'Nuevas observaciones')

    def test_crear_cita_sin_fecha(self):
        form_data = {
            'usuaria': self.user.id,
            'receta_acido_folico': False,
            'observaciones': 'Ninguna',
            'trimestre': 1
        }
        form = CitaMedicinaFamiliaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('fecha' in form.errors)

    def test_eliminar_cita(self):
        cita = CitaMedicinaFamilia.objects.get(id=self.cita.id)
        cita.delete()
        with self.assertRaises(CitaMedicinaFamilia.DoesNotExist):
            CitaMedicinaFamilia.objects.get(id=self.cita.id)