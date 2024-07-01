from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class CitaObstetraForm(forms.Form):
    fecha = forms.DateTimeField(input_formats=['%Y/%m/%d   %H:%M'],  widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    peso = forms.FloatField(required=False,widget=forms.NumberInput(attrs={'min': 0.0, 'max': 200.0}))
    altura=forms.FloatField(required=False,widget=forms.NumberInput(attrs={'min': 0.0, 'max': 2.0}))
    imc=forms.FloatField(required=False)
    tas = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'min': 0, 'max': 300}))
    tad = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'min': 0, 'max': 200}))
    trimestre = forms.IntegerField(required=False,validators=[MinValueValidator(1), MaxValueValidator(3)])
    orden = forms.IntegerField(required=False,validators=[MinValueValidator(1), MaxValueValidator(2)])
    observaciones=forms.CharField(widget=forms.Textarea,required=False)
    #40semanas
    monitores=forms.CharField(widget=forms.Textarea,required=False)

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha

    def clean_peso(self):
        peso = self.cleaned_data['peso']
        return peso

    def clean_altura(self):
        altura = self.cleaned_data['altura']
        return altura

    def clean_tas(self):
        tas = self.cleaned_data['tas']
        return tas

    def clean_tad(self):
        tad = self.cleaned_data['tad']
        return tad

    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        return observaciones