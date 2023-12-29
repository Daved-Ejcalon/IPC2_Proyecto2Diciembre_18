from django import forms
from .models import Cliente, Producto, Factura
from django.core.exceptions import ValidationError

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

        widgets = {
            'nit': forms.TextInput(attrs={'class': 'yellow-color', 'placeholder': 'XXXX XXXX XXXX XXXX'}),
            'nombre': forms.TextInput(attrs={'class': 'yellow-color', 'placeholder': 'Nombre completo'}),
            'direccion': forms.TextInput(attrs={'class': 'yellow-color', 'placeholder': 'Direccion completa'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'red-color', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.TextInput(attrs={'class': 'red-color', 'placeholder': 'Descripcion del producto'}),
            'precio': forms.TextInput(attrs={'class': 'red-color', 'placeholder': 'XX.XX', 'type': 'number'}),
            'stock': forms.TextInput(attrs={'class': 'red-color', 'placeholder': 'XX...', 'type': 'number'}),
        }


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['maestro', 'detalle', 'cliente']

        widgets = {
            'maestro': forms.TextInput(attrs={'class': 'blue-color', 'placeholder': 'Maestro de la factura'}),
            'detalle': forms.Textarea(attrs={'class': 'blue-color', 'placeholder': 'producto, cantidad\nproducto, cantidad\n.....   , .....'}),
            'cliente': forms.Select(attrs={'class': 'blue-color'}),
        }

    def clean_detalle(self):
        detalle = self.cleaned_data['detalle']
        lines = detalle.split('\n')

        productos_vendidos = []

        for line in lines:
            # Dividir cada línea en producto y cantidad
            parts = line.split(',')

            if len(parts) != 2:
                raise ValidationError('Cada línea del detalle debe tener el formato "producto, cantidad".')

            producto_nombre = parts[0].strip()
            cantidad = parts[1].strip()

            # Verificar si el producto existe en la base de datos
            try:
                producto = Producto.objects.get(nombre=producto_nombre)
            except Producto.DoesNotExist:
                raise ValidationError(f'El producto "{producto_nombre}" no está registrado en la base de datos.')

            # Actualizar el stock del producto
            nuevo_stock = producto.stock - int(cantidad)
            if nuevo_stock < 0:
                raise ValidationError(f'No hay suficiente stock para el producto "{producto_nombre}".')

            producto.stock = nuevo_stock
            productos_vendidos.append(producto)

        # Actualizar el stock de los productos vendidos
        for producto in productos_vendidos:
            producto.save() # Actualizar el producto en la base de datos

        return detalle

class BusquedaFacturaForm(forms.Form):
    busqueda = forms.CharField(max_length=50, required=False, label='Busqueda por maestro',
                                widget=forms.TextInput(
                                   attrs={'class': 'form-field', 'placeholder': 'Buscar...'}
                                ))
    
class BusquedaProductoForm(forms.Form):
    busqueda = forms.CharField(max_length=50, required=False, label='Busqueda por nombre',
                                widget=forms.TextInput(
                                   attrs={'class': 'form-field', 'placeholder': 'Buscar...'}
                                ))
    
class BusquedaClienteForm(forms.Form):
    busqueda = forms.CharField(max_length=50, required=False, label='Busqueda por nit',
                                widget=forms.TextInput(
                                   attrs={'class': 'form-field', 'placeholder': 'Buscar...'}
                                ))