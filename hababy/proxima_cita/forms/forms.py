from django import forms


class ProximaCitaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha

    
