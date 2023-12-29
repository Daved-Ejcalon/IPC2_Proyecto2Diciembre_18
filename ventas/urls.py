from django.urls import path
from django.contrib import admin
from . import views

app_name = 'ventas'


#urlconf
urlpatterns = [
    path('template', views.template, name='vacio'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('clientes/', views.clientes, name='clientes'),
    path('facturas/', views.facturas, name='facturas'),

    # Borrar registros
    path('facturas/borrar/<int:factura_id>/', views.borrar_factura, name='borrar_factura'),
    path('clientes/borrar/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
    path('productos/borrar/<int:producto_id>/', views.borrar_producto, name='borrar_producto'),

    # Editar registros
    path('facturas/editar/<int:factura_id>/', views.editar_factura, name='editar_factura'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),

    # Reportes
    path('reportes/productos', views.reportes_productos, name='reportes_productos'),
    path('reportes/clientes', views.reportes_clientes, name='reportes_clientes'),
]