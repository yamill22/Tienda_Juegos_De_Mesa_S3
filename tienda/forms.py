from django import forms


class FormVenta(forms.Form):
    nombre_cliente = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    correo = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    telefono = forms.CharField(
        label='Teléfono',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    cantidad = forms.IntegerField(
        label='Cantidad',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5,
        }),
    )

    def __init__(self, *args, juego, **kwargs):
        self.juego = juego
        super().__init__(*args, **kwargs)

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']

        if cantidad > self.juego.stock:
            raise forms.ValidationError(
                f'Solo hay {self.juego.stock} unidades disponibles.'
            )

        return cantidad