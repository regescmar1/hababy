from django import forms

class CitaOdontologiaForm(forms.Form):
    fecha = forms.DateTimeField(input_formats=['%A/%m/%d   %H:%M'],  widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    limpieza = forms.BooleanField(required=False)
    observaciones = forms.CharField(widget=forms.Textarea,required=False)
    eliminar_cita_odontologia_id=forms.IntegerField(required=False, widget=forms.HiddenInput())
    
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha

    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        return observaciones