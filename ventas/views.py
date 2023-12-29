from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import Cliente, Producto, Factura, save_to_xml
from . import forms


def home(request):
    return render(request, 'home.html')


def template(request):
    return render(request, 'template.html')

# PRODUCTOS

def productos(request):

    formualario = forms.ProductoForm()
    formulario_busqueda = forms.BusquedaProductoForm(request.GET)

    if request.method == 'POST':
        formulario = forms.ProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()  # Guardar en la base de datos
            # Guardar en el archivo XML
            save_to_xml()
            messages.success(request, 'El producto se ha creado con éxito.')
            return redirect('ventas:productos')
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')
            return redirect('ventas:productos')

    if request.method == 'GET':
        orden = request.GET.get('orden', 'normal')

        productos = Producto.objects.all()

        # Lógica para ordenar los productos según el campo seleccionado
        if orden.lower() == 'nombre':
            productos = Producto.objects.all().order_by('nombre')
        elif orden.lower() == 'precio':
            productos = Producto.objects.all().order_by('precio')
        elif orden.lower() == 'stock':
            productos = Producto.objects.all().order_by('stock')

        # Lógica para realizar la búsqueda exacta por nombre
        if formulario_busqueda.is_valid():
            busqueda = formulario_busqueda.cleaned_data['busqueda']
            if busqueda:
                productos = productos.filter(nombre__iexact=busqueda)

        # Renderizar la plantilla con la lista de productos ordenada
        formulario = forms.ProductoForm()
        return render(request, 'productos.html', {'form': formulario, 'form_busqueda': formulario_busqueda, 'datos': productos, 'campo_orden': orden})

    productos = Producto.objects.all()
    return render(request, 'productos.html', {'form': formualario, 'datos': productos, 'campo_orden': 'normal'})

def borrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    # Guardar en el archivo XML
    save_to_xml()
    return redirect('ventas:productos')

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = forms.ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            # Guardar en el archivo XML
            save_to_xml()
            messages.success(request, 'El producto se ha editado con éxito.')
            return redirect('ventas:productos')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')
            return redirect('ventas:productos')
    else:
        form = forms.ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

# CLIENTES

def clientes(request):
    formulario = forms.ClienteForm()
    formulario_busqueda = forms.BusquedaClienteForm(request.GET)

    if request.method == 'POST':
        formulario = forms.ClienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()  # Guardar en la base de datos
            # Guardar en el archivo XML
            save_to_xml()
            messages.success(request, 'El cliente se ha creado con éxito.')
            return redirect('ventas:clientes')
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')
            return redirect('ventas:clientes')

    if request.method == 'GET':
        orden = request.GET.get('orden', 'normal')

        clientes = Cliente.objects.all()

        # Lógica para ordenar los clientes según el campo seleccionado
        if orden.lower() == 'nombre':
            clientes = Cliente.objects.all().order_by('nombre')
        elif orden.lower() == 'direccion':
            clientes = Cliente.objects.all().order_by('direccion')
        elif orden.lower() == 'nit':
            clientes = Cliente.objects.all().order_by('nit')

        # Lógica para realizar la búsqueda exacta por nit
        if formulario_busqueda.is_valid():
            busqueda = formulario_busqueda.cleaned_data['busqueda']
            if busqueda:
                clientes = clientes.filter(nit__iexact=busqueda)

        # Renderizar la plantilla con la lista de clientes ordenada
        formulario = forms.ClienteForm()
        return render(request, 'clientes.html', {'form': formulario, 'form_busqueda': formulario_busqueda, 'datos': clientes, 'campo_orden': orden})

    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'form': formulario, 'datos': clientes, 'campo_orden': 'normal'})

def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    # Guardar en el archivo XML
    save_to_xml()
    return redirect('ventas:clientes')

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = forms.ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            # Guardar en el archivo XML
            save_to_xml()
            messages.success(request, 'El cliente se ha editado con éxito.')
            return redirect('ventas:clientes')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')
            return redirect('ventas:clientes')
    else:
        form = forms.ClienteForm(instance=cliente)

    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})

# FACTURAS
def facturas(request):
    formulario = forms.FacturaForm()
    formulario_busqueda = forms.BusquedaFacturaForm(request.GET)

    if request.method == 'POST':
        formulario = forms.FacturaForm(request.POST)
        if formulario.is_valid():
            cliente_proveido = formulario.cleaned_data['cliente']
            if cliente_proveido is None:
                formulario.cleaned_data['cliente'] = 'CF'
            formulario.save()
            # Guardar en el archivo XML
            save_to_xml()
            messages.success(request, 'La factura se ha creado con éxito.')
            return redirect('ventas:facturas')
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')
            return redirect('ventas:facturas')

    if request.method == 'GET':
        orden = request.GET.get('orden', 'normal')
        busqueda = request.GET.get('busqueda', '')

        facturas = Factura.objects.all()

        # Lógica para ordenar las facturas según el campo seleccionado
        if orden.lower() == 'maestro':
            facturas = Factura.objects.all().order_by('maestro')
        elif orden.lower() == 'fecha_factura':
            facturas = Factura.objects.all().order_by('fecha')

        # Lógica para realizar la búsqueda exacta por maestro
        if formulario_busqueda.is_valid():
            busqueda = formulario_busqueda.cleaned_data['busqueda']
            if busqueda:
                facturas = facturas.filter(maestro__iexact=busqueda)

        # Renderizar la plantilla con la lista de facturas ordenada
        formulario = forms.FacturaForm()
        return render(request, 'facturas.html', {'form': formulario, 'form_busqueda': formulario_busqueda, 'datos': facturas, 'campo_orden': orden})

    
    facturas = Factura.objects.all()
    return render(request, 'facturas.html', {'form': formulario, 'datos': facturas, 'campo_orden': 'normal'})

def borrar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    factura.delete()
    # Guardar en el archivo XML
    save_to_xml()
    return redirect('ventas:facturas')

def editar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    if request.method == 'POST':
        form = forms.FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            # Guardar en el archivo XML
            save_to_xml()
            messages.success(request, 'La factura se ha editado con éxito.')
            return redirect('ventas:facturas')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')
            return redirect('ventas:facturas')
    else:
        form = forms.FacturaForm(instance=factura)

    return render(request, 'editar_factura.html', {'form': form, 'factura': factura})

# REPORTES
def reportes_productos(request):

    facturas = Factura.objects.all()

    # 10 productos más vendidos
    productos = {}
    for factura in facturas:
        detalle = factura.detalle.split('\n')
        for producto in detalle:
            nombre, cantidad = producto.split(',')
            if nombre in productos:
                productos[nombre] += int(cantidad)
            else:
                productos[nombre] = int(cantidad)

    # Ordenar
    productos = sorted(productos.items(), key=lambda x: x[1], reverse=True)[:10]

    # Obtener nombres y cantidades
    nombres_productos = [producto[0] for producto in productos]
    cantidades = [producto[1] for producto in productos]

    return render(request, 'reporte_productos.html', {'nombres_productos': nombres_productos, 'cantidades': cantidades})


def reportes_clientes(request):
    facturas = Factura.objects.all()
    compras_por_cliente = {}

    #total de compras para cada cliente
    for factura in facturas:
        cliente = factura.cliente

        print(cliente)

        if cliente is None:
            cliente = 'CF'
        else:
            cliente = cliente.nombre

        # Actualiza el diccionario de compras_por_cliente
        if cliente in compras_por_cliente:
            compras_por_cliente[cliente] += 1
        else:
            compras_por_cliente[cliente] = 1

    # Ordena los clientes
    clientes_ordenados = sorted(compras_por_cliente.items(), key=lambda x: x[1], reverse=True)

    # Obtener nombres y cantidades
    nombres_clientes = [str(cliente[0]) for cliente in clientes_ordenados]
    cantidades_compras = [cliente[1] for cliente in clientes_ordenados]

    return render(request, 'reporte_clientes.html', {'nombres_clientes': nombres_clientes, 'cantidades_compras': cantidades_compras})