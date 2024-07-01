from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class CitaExtraccionesForm(forms.Form):
    fecha = forms.DateTimeField(input_formats=['%Y/%m/%d   %H:%M'],  widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    analisis_normal=forms.BooleanField(required=False)
    test_o_sullivan_positivo=forms.BooleanField(required=False)
    rh_negativo=forms.BooleanField(required=False)
    anemia=forms.BooleanField(required=False)
    observaciones=forms.CharField(widget=forms.Textarea,required=False)
    trimestre = forms.IntegerField(required=False,validators=[MinValueValidator(1), MaxValueValidator(3)])

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha

    def clean_analisis_normal(self):
        analisis_normal = self.cleaned_data['analisis_normal']
        return analisis_normal

    def clean_test_o_sullivan_positivo(self):
        test_o_sullivan_positivo = self.cleaned_data['test_o_sullivan_positivo']
        return test_o_sullivan_positivo

    def clean_rh_negativo(self):
        rh_negativo = self.cleaned_data['rh_negativo']
        return rh_negativo

    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        return observaciones

class CurvaLargaForm(forms.Form):
    fecha = forms.DateTimeField(input_formats=['%Y/%m/%d   %H:%M'],  widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    analisis_normal=forms.BooleanField(required=False)
    observaciones=forms.CharField(widget=forms.Textarea,required=False)
    trimestre = forms.IntegerField(required=False,validators=[MinValueValidator(1), MaxValueValidator(3)])
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha

    def clean_analisis_normal(self):
        analisis_normal = self.cleaned_data['analisis_normal']
        return analisis_normal

    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        return observaciones