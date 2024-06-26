from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class CitaMedicinaFamiliaForm(forms.Form):
    fecha = forms.DateTimeField(input_formats=['%Y/%m/%d   %H:%M'],  widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    receta_acido_folico=forms.BooleanField(required=False)
    receta_hierro=forms.BooleanField(required=False)
    observaciones=forms.CharField(widget=forms.Textarea,required=False)
    trimestre = forms.IntegerField(required=False,validators=[MinValueValidator(1), MaxValueValidator(3)])

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha
    
    def clean_receta_acido_folico(self):
        receta_acido_folico = self.cleaned_data['receta_acido_folico']
        return receta_acido_folico
    
    def clean_receta_hierro(self):
        receta_hierro=self.cleaned_data['receta_hierro']
        return receta_hierro
    
    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        return observaciones