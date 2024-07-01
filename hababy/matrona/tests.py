import datetime
from django.test import TestCase
from matrona.models import CitaMatrona
from django.contrib.auth.models import User
from django.utils import timezone
from matrona.forms.forms import CitaMatronaForm

class MatronaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.cita = CitaMatrona.objects.create(
            usuaria=self.user,
            fecha=timezone.make_aware(datetime.datetime(2024, 3, 25, 8, 0, 0), timezone=timezone.get_current_timezone()),
            peso=70.5,
            altura=1.75,
            imc=23.0,
            tas=120,
            tad=80,
            trimestre=2,
            orden=1,
            exploracion_obstetrica="exploracion",
            egb=True
        )

    def test_crear_cita(self):
        cita = CitaMatrona.objects.get(id=self.cita.id)
        self.assertEqual(cita.usuaria, self.user)
        self.assertAlmostEqual(cita.peso, 70.5)
        self.assertAlmostEqual(cita.altura, 1.75)
        self.assertAlmostEqual(cita.imc, 23.0)
        self.assertEqual(cita.tas, 120)
        self.assertEqual(cita.tad, 80)
        self.assertEqual(cita.trimestre, 2)
        self.assertEqual(cita.orden, 1)
        self.assertEqual(cita.exploracion_obstetrica,"exploracion")
        self.assertEqual(cita.egb,True)

    def test_actualizar_cita(self):
        cita = CitaMatrona.objects.get(id=self.cita.id)
        cita.fecha = timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone())
        cita.peso = 60.0
        cita.altura = 1.6
        cita.tas = 100
        cita.tad = 60
        cita.exploracion_obstetrica="abc"
        cita.egb=False
        cita.save()
        updated_cita = CitaMatrona.objects.get(id=self.cita.id)
        self.assertEqual(updated_cita.fecha, timezone.make_aware(datetime.datetime(2024, 3, 26, 9, 0, 0), timezone=timezone.get_current_timezone()))
        self.assertEqual(updated_cita.peso,cita.peso)
        self.assertEqual(updated_cita.altura,cita.altura)
        self.assertEqual(updated_cita.tas,cita.tas)
        self.assertEqual(updated_cita.tad,cita.tad)
        self.assertEqual(updated_cita.exploracion_obstetrica,cita.exploracion_obstetrica)
        self.assertEqual(updated_cita.egb,cita.egb)

    def test_crear_cita_sin_fecha(self):
        form_data = {
            'usuaria': self.user.id,
            'peso': 70.5,
            'altura': 1.75,
            'tas': 120,
            'tad': 80,
            'trimestre': 2,
            'orden': 1,
            'exploracion_obstetrica':"abc",
            'egb':True
        }
        form = CitaMatronaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('fecha' in form.errors)

    def test_eliminar_cita(self):
        cita = CitaMatrona.objects.get(id=self.cita.id)
        cita.delete()
        with self.assertRaises(CitaMatrona.DoesNotExist):
            CitaMatrona.objects.get(id=self.cita.id)