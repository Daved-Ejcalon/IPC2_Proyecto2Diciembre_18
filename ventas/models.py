from django.db import models
import xml.etree.ElementTree as ET
from django.apps import apps
from django.db.models import Model
from xml.dom import minidom

# Create your models here.

class Cliente(models.Model):
    nit = models.CharField(max_length=13, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nit} - {self.nombre} - {self.direccion}"

    def to_xml(self):
        # Construye y devuelve la representación XML del objeto
        xml_data = ET.Element("producto")
        ET.SubElement(xml_data, "nombre").text = self.nombre
        ET.SubElement(xml_data, "descripcion").text = self.descripcion
        ET.SubElement(xml_data, "precio").text = str(self.precio)
        ET.SubElement(xml_data, "stock").text = str(self.stock)

        return ET.tostring(xml_data, encoding="unicode")

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.precio} - {self.stock}"

    def to_xml(self):
        # Construye y devuelve la representación XML del objeto
        xml_data = ET.Element("producto")
        ET.SubElement(xml_data, "nombre").text = self.nombre
        ET.SubElement(xml_data, "descripcion").text = self.descripcion
        ET.SubElement(xml_data, "precio").text = str(self.precio)
        ET.SubElement(xml_data, "stock").text = str(self.stock)

        return ET.tostring(xml_data, encoding="unicode")
    
class Factura(models.Model):
    maestro = models.CharField(max_length=100, unique=True)
    detalle = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, to_field="nit", default="CF", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.maestro} - {self.fecha}\n{self.detalle}"
    
    def to_xml(self):
        # Construye y devuelve la representación XML del objeto
        xml_data = ET.Element("factura")
        ET.SubElement(xml_data, "maestro").text = self.maestro
        ET.SubElement(xml_data, "detalle").text = self.detalle
        ET.SubElement(xml_data, "fecha").text = str(self.fecha)
        ET.SubElement(xml_data, "cliente").text = str(self.cliente)

        return ET.tostring(xml_data, encoding="unicode")


def save_to_xml():
    # Obtén todos los modelos de la aplicación
    models = apps.get_models()

    # Crea el elemento raíz <datos>
    root = ET.Element("datos")

    # Itera sobre los modelos y crea elementos <listaModelo> para cada uno
    for model in models:
        if issubclass(model, Model):
            model_name = model.__name__
            if model_name == "Factura" or model_name == "Cliente" or model_name == "Producto":
                lista_modelo = ET.SubElement(root, f"lista{model_name}")

                # Obtén todos los objetos del modelo
                objects = model.objects.all()

                # Itera sobre los objetos y crea elementos para cada uno
                for obj in objects:
                    model_element = ET.SubElement(lista_modelo, model_name.lower())

                    # Añade atributos según el modelo
                    for field in obj._meta.fields:
                        field_name = field.name
                        field_value = getattr(obj, field_name)

                        # Si es el campo 'detalle' de la factura, reemplaza saltos de línea por espacio
                        if model_name.lower() == 'factura' and field_name.lower() == 'detalle':
                            field_value = field_value.replace('\n', ' ')

                        ET.SubElement(model_element, field_name).text = str(field_value)

    # Convierte el árbol XML a una cadena con formato
    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    # Guarda el contenido en el archivo
    with open("datos.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
