from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class GestionCitasTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_gestion_citas(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('gestion_citas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gestion_citas.html')


    def test_citas_primer(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('citas_primer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'citas_primer.html')


    
    def test_citas_segundo(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('citas_segundo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'citas_segundo.html')


    def test_citas_tercer(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('citas_tercer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'citas_tercer.html')